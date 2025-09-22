import unittest

from s3_reader.reader import S3Reader

class TestS3Reader(unittest.TestCase):
    def test_init(self):
        reader = S3Reader("rewaj-cb-tf", "base_json/2025-09-15T12-00.jsonl")
        self.assertEquals(reader.bucket_name, "rewaj-cb-tf")
        self.assertTrue(reader.file_directory, "base_json/2025-09-15T12-00.jsonl")
        reader.close()

    def test_get_next_line(self):
        reader = S3Reader("rewaj-cb-tf", "base_json/2025-09-15T12-00.jsonl")
        first_line = reader.get_next_line()
        self.assertEquals(first_line,
                          '{"ts":"2025-09-15T12:00:01Z","service":"orders","level":"INFO","msg":"new order received","orderId":"o-123"}\n')

        second_line = reader.get_next_line()
        self.assertEquals(second_line,
                          '{"ts":"2025-09-15T12:00:03Z","service":"orders","level":"ERROR","msg":"payment declined","orderId":"o-123","customer":{"id":"c-9","region":"eu"}}\n'
        )
        reader.close()


    def test_next_line_terminates(self):
        reader = S3Reader("rewaj-cb-tf", "base_json/2025-09-15T12-00.jsonl")
        while reader.get_next_line():
            pass
        self.assertTrue(True)
        reader.close()

    def test_iterates_through_all_lines(self):
        reader = S3Reader("rewaj-cb-tf", "base_json/2025-09-15T12-00.jsonl")
        previous_line = reader.get_next_line()
        next_line = reader.get_next_line()
        number_of_lines = 1
        while next_line:
            previous_line = next_line
            next_line = reader.get_next_line()
            number_of_lines += 1
        self.assertEquals(number_of_lines, 5)
        self.assertEquals(previous_line,
                          '{"ts":"2025-09-15T12:00:09Z","service":"api","level":"INFO","msg":"GET /status 200","latency_ms":42}\n')

if __name__ == "__main__":
    unittest.main()
