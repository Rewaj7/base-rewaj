import io
import os
from datetime import datetime

import boto3

import json

from lib.aws.cloudwatch import CloudwatchMetrics

s3 = boto3.client("s3")
sns_client = boto3.client('sns')
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")


class LogAnalyzer:
    DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self,
                 threshold,
                 bucket_name=None,
                 prefix=None,
                 time_stamp=None,
                 publish_metrics=False,
                 local=None):
        """
        :param threshold: Number of error logs to trigger an alert
        :param bucket_name: S3 bucket name to find latest log files
        :param prefix: S3 Prefix to find latest log file in bucket
        :param time_stamp: Timestamp to include only logs recorded after
        :param local: Local file directory
        """
        self.threshold = threshold
        self.trigger_alert = False
        self.time_stamp = time_stamp
        self.report_json = None
        self.publish_metrics = publish_metrics
        if local:
            self.bucket_name = None
            self.file_directory = local
            self.file_body = open(self.file_directory, "rb")
        elif bucket_name and prefix:
            self.bucket_name = bucket_name
            self.file_directory = LogAnalyzer.get_most_recent_json(bucket_name,
                                                                   prefix)
            self.file_body = s3.get_object(
                Bucket=self.bucket_name,
                Key=self.file_directory)["Body"]
        else:
            raise Exception("LogAnalyzer object set with local and bucket")
        self.stream = io.TextIOWrapper(self.file_body, encoding="utf-8")

    @staticmethod
    def get_most_recent_json(bucket_name, prefix) -> str:
        """
        :param bucket_name: S3 bucket name to find latest log files
        :param prefix: S3 Prefix to find latest log file in bucket
        :return: The S3 object key of the most last log file
        """
        latest_file = None
        latest_time = None

        s3 = boto3.client('s3')
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
            for obj in page["Contents"]:
                key = obj["Key"]
                filename = key.split("/")[-1]
                timestamp_str = filename.replace(".jsonl", "")
                if filename != "":
                    timestamp = datetime.strptime(timestamp_str,
                                                  "%Y-%m-%dT%H-%M")
                    if latest_time is None or timestamp > latest_time:
                        latest_time = timestamp
                        latest_file = key

        return latest_file

    def get_next_line(self):
        while True:
            line = self.stream.readline()
            if line == '':  # EOF
                return None
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                return line

    def get_next_json_line(self):
        while True:
            next_line = self.get_next_line()
            if next_line is None:  # EOF
                return None
            try:
                return json.loads(next_line)
            except json.JSONDecodeError:
                continue

    def close(self):
        self.stream.close()

    def is_next_error(self):
        """
        :return: A dict with:
        - "service_name": the service that made the log (N/A if no next line)
        - "is_error": if the log corresponds to an error. -1 If no next line
        """
        next_line = self.get_next_json_line()
        service = next_line["service"] if next_line else "N/A"
        is_error = -1
        if next_line:
            log_dt = datetime.strptime(
                next_line["ts"],
                LogAnalyzer.DATE_TIME_FORMAT)
            after_timestamp = not self.time_stamp or log_dt > self.time_stamp
            is_error = int(next_line["level"] == "ERROR" and after_timestamp)
            if next_line["level"] == "ERROR" and self.publish_metrics:
                CloudwatchMetrics.push_error_metrics(
                    timestamp=next_line["ts"],
                    service=next_line["service"])

        return {
            "service": service,
            "is_error": is_error
        }

    def generate_report(self, notify_sns: bool = False):
        """
        :param notify_sns: Whether to send SNS message if errors pass threshold
        :return: JSON report
        """
        number_of_errors = {}
        total_errors = 0
        is_next_error = self.is_next_error()
        is_error = is_next_error["is_error"]
        service = is_next_error["service"]
        while is_error >= 0:
            total_errors += int(is_error)
            if service in number_of_errors:
                number_of_errors[service] += int(is_error)
            elif is_error >= 1:
                number_of_errors[service] = 1
            is_next_error = self.is_next_error()
            is_error = is_next_error["is_error"]
            service = is_next_error["service"]
        return_json = {"byService": number_of_errors, "total": total_errors}
        if total_errors >= self.threshold:
            return_json["alert"] = "true"
            self.trigger_alert = True
            if notify_sns:
                self.publish_sns(total_errors)
            if self.publish_metrics:
                CloudwatchMetrics.push_alert_metric()
        return return_json

    def publish_sns(self, total_errors: int):
        message = "S3 Logs Error Alert"
        message_attributes = {
            'file_directory': {
                'DataType': 'String',
                'StringValue': self.file_directory
            },
            'number_of_alerts': {
                'DataType': 'Number',
                'StringValue': str(total_errors)
            }
        }

        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            MessageAttributes=message_attributes,
            Subject='S3 Logs Error Alert'
        )

        print("Message ID:", response['MessageId'])
