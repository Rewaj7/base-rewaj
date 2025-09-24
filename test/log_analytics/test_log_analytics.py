import unittest
from datetime import datetime

from lib.log_analytics.analyzer import LogAnalyzer


class TestLogAnalyzer(unittest.TestCase):

    def test_s3_init(self):
        analyzer = LogAnalyzer(
            bucket_name="devops-assignment-logs-19-08",
            prefix="tests/2025-09-15T12",
            threshold=5)
        self.assertEqual(analyzer.bucket_name, "devops-assignment-logs-19-08")
        self.assertTrue(analyzer.file_directory, "tests/2025-09-15T12-00.jsonl")
        analyzer.close()

    def test_s3_get_next_line(self):
        analyzer = LogAnalyzer(
            bucket_name="devops-assignment-logs-19-08",
            prefix="tests/2025-09-15T12-00.jsonl",
            threshold=5)
        first_line = analyzer.get_next_line()
        self.assertEqual(first_line,
                          '{"ts":"2025-09-15T12:00:01Z","service":"orders","level":"INFO","msg":"new order received","orderId":"o-123"}\n')

        second_line = analyzer.get_next_line()
        self.assertEqual(second_line,
                          '{"ts":"2025-09-15T12:00:03Z","service":"orders","level":"ERROR","msg":"payment declined","orderId":"o-123","customer":{"id":"c-9","region":"eu"}}\n'
        )
        analyzer.close()

    def test_s3_gets_recent_file(self):
        analyzer = LogAnalyzer(
            bucket_name="devops-assignment-logs-19-08",
            prefix="tests",
            threshold=5)
        self.assertEqual(analyzer.file_directory, "tests/2025-09-15T16-00.jsonl")
        analyzer.close()

    def test_local_get_next_line(self):
        analyzer = LogAnalyzer(
            local="./test/test_cases/2025-09-15T12-00.jsonl",
            threshold=5)
        first_line = analyzer.get_next_line()
        self.assertEqual(first_line,
                          '{"ts":"2025-09-15T12:00:01Z","service":"orders","level":"INFO","msg":"new order received","orderId":"o-123"}\n')

        second_line = analyzer.get_next_line()
        self.assertEqual(second_line,
                          '{"ts":"2025-09-15T12:00:03Z","service":"orders","level":"ERROR","msg":"payment declined","orderId":"o-123","customer":{"id":"c-9","region":"eu"}}\n'
        )
        analyzer.close()


    def test_next_line_terminates(self):
        analyzer = LogAnalyzer(
            local="./test/test_cases/2025-09-15T12-00.jsonl",
            threshold=5)
        while analyzer.get_next_line():
            pass
        self.assertTrue(True)
        analyzer.close()

    def test_iterates_through_all_lines(self):
        analyzer = LogAnalyzer(
            local="./test/test_cases/2025-09-15T12-00.jsonl",
            threshold=5)
        previous_line = analyzer.get_next_line()
        next_line = analyzer.get_next_line()
        number_of_lines = 1
        while next_line:
            previous_line = next_line
            next_line = analyzer.get_next_line()
            number_of_lines += 1
        self.assertEqual(number_of_lines, 5)
        self.assertEqual(previous_line,
                          '{"ts":"2025-09-15T12:00:09Z","service":"api","level":"INFO","msg":"GET /status 200","latency_ms":42}\n')

        analyzer.close()


    def test_get_next_json_line(self):
        analyzer = LogAnalyzer(
            local="./test/test_cases/2025-09-15T12-00.jsonl",
            threshold=5)
        first_json_line = analyzer.get_next_json_line()
        self.assertEqual(first_json_line["service"], "orders")
        self.assertEqual(first_json_line["msg"], "new order received")

        second_json_line = analyzer.get_next_json_line()
        self.assertEqual(second_json_line["service"], "orders")
        self.assertEqual(second_json_line["msg"], "payment declined")

        analyzer.close()

    def test_is_next_line_error(self):
        analyzer = LogAnalyzer(
            bucket_name="devops-assignment-logs-19-08",
            prefix="tests/2025-09-15T12-00.jsonl",
            threshold=5)
        first_error = analyzer.is_next_error()
        self.assertFalse(first_error["is_error"])

        second_error = analyzer.is_next_error()
        self.assertTrue(second_error["is_error"])

        third_error = analyzer.is_next_error()
        self.assertFalse(third_error["is_error"])

        fourth_error = analyzer.is_next_error()
        self.assertTrue(fourth_error["is_error"])

        analyzer.close()

    def test_number_of_errors(self):
        analyzer = LogAnalyzer(
            bucket_name="devops-assignment-logs-19-08",
            prefix="tests/2025-09-15T12-00.jsonl",
            threshold=5)
        report = analyzer.generate_report()
        self.assertEqual(report["total"], 2)
        self.assertEqual(report["byService"]["orders"], 1)
        self.assertEqual(report["byService"]["billing"], 1)
        self.assertNotIn("api",report["byService"])

        analyzer.close()

    def test_alert_threshold(self):
        high_threshold = LogAnalyzer(bucket_name="devops-assignment-logs-19-08",
                                     prefix="tests/2025-09-15T12",
                                     threshold=5)
        high_threshold_json = high_threshold.generate_report()
        self.assertNotIn("alert",high_threshold_json)
        high_threshold.close()

        low_threshold = LogAnalyzer(bucket_name="devops-assignment-logs-19-08",
                                    prefix="tests/2025-09-15T12",
                                    threshold=2)
        low_threshold_json = low_threshold.generate_report()
        self.assertEqual("true",low_threshold_json["alert"])
        low_threshold.close()

    def test_number_of_errors_with_since(self):
        analyzer = LogAnalyzer(bucket_name="devops-assignment-logs-19-08",
                               prefix="tests/2025-09-15T12",
                               threshold=2,
                               time_stamp=datetime.strptime("2025-09-15T12:00:05Z", LogAnalyzer.DATE_TIME_FORMAT))
        report_json = analyzer.generate_report()
        self.assertEqual(report_json["total"], 1)
        self.assertNotIn("orders",report_json["byService"])
        self.assertEqual(report_json["byService"]["billing"], 1)
        self.assertNotIn("alert",report_json)

        analyzer.close()


    def test_get_next_json_line_skips_malformed(self):
        analyzer = LogAnalyzer(
            local="./test/test_cases/2025-09-15T13-00.jsonl",
            threshold=5
        )

        first_json = analyzer.get_next_json_line()
        self.assertEqual(first_json["service"], "orders")
        self.assertEqual(first_json["msg"], "new order received")

        second_json = analyzer.get_next_json_line()
        self.assertEqual(second_json["service"], "orders")
        self.assertEqual(second_json["msg"], "inventory shortfall")

        third_json = analyzer.get_next_json_line()
        self.assertEqual(third_json["service"], "billing")
        self.assertEqual(third_json["msg"], "charge succeeded")

        fourth_json = analyzer.get_next_json_line()
        self.assertEqual(fourth_json["service"], "billing")
        self.assertEqual(fourth_json["msg"], "rate limit exceeded")

        fifth_json = analyzer.get_next_json_line()
        self.assertEqual(fifth_json["service"], "shipping")
        self.assertEqual(fifth_json["msg"], "shipment queued")

        sixth_json = analyzer.get_next_json_line()
        self.assertEqual(sixth_json["service"], "shipping")
        self.assertEqual(sixth_json["msg"], "label printer offline")

        self.assertIsNone(analyzer.get_next_json_line())
        analyzer.close()


    def test_generate_report_skips_malformed(self):
        analyzer = LogAnalyzer(
            local="./test/test_cases/2025-09-15T13-00.jsonl",
            threshold=5
        )
        report_json = analyzer.generate_report()
        self.assertEqual(report_json["total"], 3)

        analyzer.close()

    def test_generate_report_skips_malformed_value(self):
        analyzer = LogAnalyzer(
            local="./test/test_cases/2025-09-15T16-00.jsonl",
            threshold=5
        )
        report_json = analyzer.generate_report()
        self.assertEqual(report_json["total"], 112)

        analyzer.close()

