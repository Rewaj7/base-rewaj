import argparse
import datetime

from lib.log_analytics.analyzer import LogAnalyzer


def parse_iso8601(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        error_message = f"Not a valid ISO 8601 timestamp: '{s}'. Expected format YYYY-MM-DDTHH:MM:SSZ"
        raise argparse.ArgumentTypeError(error_message)

def main():
    parser = argparse.ArgumentParser(prog="analyze", description="Analyze CLI tool")
    # Required arguments
    parser.add_argument(
        "--bucket",
        type=str,
        required=True,
        help="Name of the S3 bucket"
    )
    parser.add_argument(
        "--prefix",
        type=str,
        required=True,
        help="Prefix/folder in the bucket"
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
        help="Only process logs newer than this ISO 8601 timestamp (e.g., 2025-09-15T12:00:01Z)"
    )

    args = parser.parse_args()
    log_analyzer = LogAnalyzer(args.bucket, args.prefix, args.threshold, args.since)
    report = log_analyzer.generate_report()
    print(report)
    return report


if __name__ == "__main__":
    main()