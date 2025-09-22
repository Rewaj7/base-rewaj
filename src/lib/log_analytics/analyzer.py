from datetime import datetime

from lib.s3_reader.reader import S3Reader
import json


class LogAnalyzer:
    DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, bucket_name, file_directory, threshold, time_stamp = None):
        self.s3_reader = S3Reader(bucket_name=bucket_name, file_directory=file_directory)
        self.threshold = threshold
        self.trigger_alert = False
        self.time_stamp = time_stamp
        self.report_json = None

    def get_next_json_line(self):
        next_line = self.s3_reader.get_next_line()
        return json.loads(next_line) if next_line else None

    def close(self):
        self.s3_reader.close()

    def is_next_error(self):
        next_line = self.get_next_json_line()
        service = next_line["service"] if next_line else "N/A"
        is_error = -1
        if next_line:
            after_timestamp = not self.time_stamp or datetime.strptime(next_line["ts"], LogAnalyzer.DATE_TIME_FORMAT) > self.time_stamp
            is_error = int(next_line["level"] == "ERROR" and after_timestamp)

        return {
            "service": service,
            "is_error": is_error
        }

    def generate_report(self):
        self.report_json = self.number_of_errors()
        return self.report_json

    def number_of_errors(self):
        number_of_errors = {}
        total_errors = 0
        is_next_error = self.is_next_error()
        while is_next_error["is_error"] >= 0:
            total_errors += int(is_next_error["is_error"])
            if is_next_error["service"] in number_of_errors:
                number_of_errors[is_next_error["service"]] += int(is_next_error["is_error"])
            elif is_next_error["is_error"] >= 1:
                number_of_errors[is_next_error["service"]] = 1
            is_next_error = self.is_next_error()
        return_json = {"byService": number_of_errors, "total": total_errors}
        if total_errors >= self.threshold:
            return_json["alert"] = "true"
            self.trigger_alert = True
        return return_json

