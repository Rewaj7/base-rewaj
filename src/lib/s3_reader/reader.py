import io
import boto3

class S3Reader:

    def __init__(self, bucket_name:str, file_directory):
        self.bucket_name = bucket_name
        self.file_directory = file_directory
        self.file_body = s3.get_object(Bucket=bucket, Key=key)["Body"]
        self.stream = io.TextIOWrapper(self.file_body, encoding="utf-8")

    def get_all_lines(self):
        return self.file_body.iter_lines()

    def get_next_line(self):
        line = self.stream.readline()
        return line if line else None

    def close(self):
        self.stream.close()


if __name__ == '__main__':
    print("Hello")

    s3 = boto3.client("s3")

    bucket = "rewaj-cb-tf"
    key = "base_json/2025-09-15T12-00.jsonl"

    reader = S3Reader(bucket_name=bucket, file_directory=key)

    current_line = reader.get_next_line()
    while current_line:
        print(current_line)
        current_line = reader.get_next_line()
    reader.close()