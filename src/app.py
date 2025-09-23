from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query
from lib.log_analytics.analyzer import LogAnalyzer

app = FastAPI()

def parse_iso8601(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        error_message = f"Not a valid ISO 8601 timestamp: '{s}'. Expected format YYYY-MM-DDTHH:MM:SSZ"
        return ValueError(error_message)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/analyze/")
async def analyze(
    bucket: str = Query(..., description="Name of the S3 bucket"),
    prefix: str = Query(..., description="Prefix/folder in the bucket"),
    threshold: int = Query(..., description="Threshold value to trigger alert"),
    since: Optional[str] = Query(None, description="Only process logs newer than timestamp")
):
    since_dt: Optional[datetime] = parse_iso8601(since) if since else None

    log_analyzer = LogAnalyzer(bucket, prefix, threshold, since_dt)
    report = log_analyzer.generate_report()
    print(report)
    return report