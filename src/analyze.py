import argparse
from datetime import datetime

from lib.log_analytics.analyzer import LogAnalyzer


def parse_iso8601(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        error_message = (f"Not a valid ISO 8601 timestamp: '{s}'. "
                         f"Expected format YYYY-MM-DDTHH:MM:SSZ")
        raise argparse.ArgumentTypeError(error_message)


def main():
    parser = argparse.ArgumentParser(
        prog="analyze",
        description="Analyze CLI tool")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--local",
        help="Use local logs instead of S3 bucket"
    )
    group.add_argument(
        "--bucket",
        type=str,
        help="Name of the S3 bucket"
    )

    parser.add_argument(
        "--prefix",
        type=str,
        help="Prefix/folder in the bucket (required if --bucket is used)"
    )

    parser.add_argument(
        "--threshold",
        type=int,
        required=True,
        help="Threshold value for analysis"
    )

    parser.add_argument(
        "--since",
        type=parse_iso8601,
        required=False,
        help="Only process logs newer than this ISO 8601 timestamp"
    )

    args = parser.parse_args()
    if args.bucket and not args.prefix:
        parser.error("--prefix is required when using --bucket")

    log_analyzer = LogAnalyzer(bucket_name=args.bucket,
                               prefix=args.prefix,
                               threshold=args.threshold,
                               local=args.local,
                               time_stamp=args.since)
    report = log_analyzer.generate_report()
    return report


if __name__ == "__main__":
    main()
