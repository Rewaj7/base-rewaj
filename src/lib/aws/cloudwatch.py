import boto3
import os
from datetime import datetime

cloudwatch = boto3.client('cloudwatch')
environment = os.environ.get("ENVIRONMENT")


class CloudwatchMetrics:

    @staticmethod
    def push_error_metrics(timestamp: str, service: str):
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        print(f"Pushing error at {timestamp} for serivce {service}")
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

        print([
                {
                    'MetricName': 'logErrors',
                    'Dimensions': [
                        {'Name': 'Service', 'Value': service},
                        {'Name': 'Environment', 'Value': environment}
                    ],
                    'Timestamp': dt,
                    'Value': 1,
                    'Unit': 'Count',
                    'StorageResolution': 1
        }
            ])

    @staticmethod
    def push_alert_metric():
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