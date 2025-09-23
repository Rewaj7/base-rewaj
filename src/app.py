from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
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
    local: str = Query(None, description="Directory of local file"),
    bucket: str = Query(None, description="Name of the S3 bucket"),
    prefix: str = Query(None, description="Prefix/folder in the bucket"),
    threshold: int = Query(..., description="Threshold value to trigger alert"),
    since: Optional[str] = Query(None, description="Only process logs newer than timestamp")
):
    since_dt: Optional[datetime] = parse_iso8601(since) if since else None

    if local:
        if bucket or prefix:
            raise HTTPException(status_code=400, detail="Cannot provide both local and bucket/prefix")
    else:
        if not (bucket and prefix):
            raise HTTPException(status_code=400, detail="Must provide either local or both bucket and prefix")


    log_analyzer = LogAnalyzer(bucket_name=bucket, prefix=prefix, threshold=threshold, time_stamp=since_dt, local=local)
    report = log_analyzer.generate_report()
    print(report)
    return report