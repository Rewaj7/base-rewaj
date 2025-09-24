import boto3
import os
from datetime import datetime

cloudwatch = boto3.client('cloudwatch')
environment = os.environ.get("ENVIRONMENT")


class CloudwatchMetrics:

    @staticmethod
    def push_error_metrics(timestamp: str, service: str):
        """
        :param timestamp: Timestamp of the error log
        :param service: Service associated with error log
        """
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        cloudwatch.put_metric_data(
            Namespace='LogAnalytics',
            MetricData=[
                {
                    'MetricName': 'logErrors',
                    'Dimensions': [
                        {'Name': 'Service', 'Value': service},
                        {'Name': 'Environment', 'Value': environment}
                    ],
                    'Timestamp': dt,
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
        )


    @staticmethod
    def push_alert_metric():
        """
        Pushes a Cloudwatch metric corresponding to a triggered alert
        """
        cloudwatch.put_metric_data(
            Namespace='LogAnalytics',
            MetricData=[
                {
                    'MetricName': 'alertTriggered',
                    'Dimensions': [
                        {'Name': 'Environment', 'Value': environment}
                    ],
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
        )