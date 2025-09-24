FROM python:3.12-slim

WORKDIR /app

COPY src/ /app/src/
COPY requirements.txt /app/

ENV PYTHONPATH=/app/src
ENV AWS_DEFAULT_REGION=eu-west-1
ENV ENVIRONMENT=dev

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
