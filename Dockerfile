FROM python:3.12-slim

WORKDIR /app

COPY src/ /app/src/
COPY requirements.txt /app/

ENV PYTHONPATH=/app/src

RUN pip install -r requirements.txt

CMD ["python", "src/analyze.py"]
