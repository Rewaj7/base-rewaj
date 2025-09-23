import unittest
from datetime import datetime

from lib.log_analytics.analyzer import LogAnalyzer


class TestLogAnalyzer(unittest.TestCase):

    def test_init(self):
        analyzer = LogAnalyzer("devops-assignment-logs-19-08", "tests/2025-09-15T12-00.jsonl", 5)
        self.assertEquals(analyzer.bucket_name, "devops-assignment-logs-19-08")
        self.assertTrue(analyzer.file_directory, "tests/2025-09-15T12-00.jsonl")
        analyzer.close()

    def test_get_next_line(self):
        reader = LogAnalyzer("devops-assignment-logs-19-08", "tests/2025-09-15T12-00.jsonl", 5)
        first_line = reader.get_next_line()
        self.assertEquals(first_line,
                          '{"ts":"2025-09-15T12:00:01Z","service":"orders","level":"INFO","msg":"new order received","orderId":"o-123"}\n')

        second_line = reader.get_next_line()
        self.assertEquals(second_line,
                          '{"ts":"2025-09-15T12:00:03Z","service":"orders","level":"ERROR","msg":"payment declined","orderId":"o-123","customer":{"id":"c-9","region":"eu"}}\n'
        )
        reader.close()


    def test_next_line_terminates(self):
        reader = LogAnalyzer("devops-assignment-logs-19-08", "tests/2025-09-15T12-00.jsonl", 5)
        while reader.get_next_line():
            pass
        self.assertTrue(True)
        reader.close()

    def test_iterates_through_all_lines(self):
        reader = LogAnalyzer("devops-assignment-logs-19-08", "tests/2025-09-15T12-00.jsonl", 5)
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


    def test_get_next_json_line(self):
        analyzer = LogAnalyzer("devops-assignment-logs-19-08", "tests/2025-09-15T12", 5)
        first_json_line = analyzer.get_next_json_line()
        self.assertEquals(first_json_line["service"], "orders")
        self.assertEquals(first_json_line["msg"], "new order received")

        second_json_line = analyzer.get_next_json_line()
        self.assertEquals(second_json_line["service"], "orders")
        self.assertEquals(second_json_line["msg"], "payment declined")

        analyzer.close()

    def test_is_next_line_error(self):
        analyzer = LogAnalyzer("devops-assignment-logs-19-08", "tests/2025-09-15T12", 5)
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
        analyzer = LogAnalyzer("devops-assignment-logs-19-08", "tests/2025-09-15T12", 5)
        analyzer.generate_report()
        number_of_errors = analyzer.report_json
        self.assertEquals(number_of_errors["total"], 2)
        self.assertEquals(number_of_errors["byService"]["orders"], 1)
        self.assertEquals(number_of_errors["byService"]["billing"], 1)
        self.assertNotIn("api",number_of_errors["byService"])

    def test_alert_threshold(self):
        high_threshold = LogAnalyzer("devops-assignment-logs-19-08", "tests/2025-09-15T12", 5)
        high_threshold.generate_report()
        high_threshold_json = high_threshold.report_json
        self.assertNotIn("alert",high_threshold_json)

        low_threshold = LogAnalyzer("devops-assignment-logs-19-08", "tests/2025-09-15T12", 2)
        low_threshold.generate_report()
        low_threshold_json = low_threshold.report_json
        self.assertEquals("true",low_threshold_json["alert"])

    def test_number_of_errors_with_since(self):
        analyzer = LogAnalyzer("devops-assignment-logs-19-08",
                               "tests/2025-09-15T12",
                               2,
                               time_stamp=datetime.strptime("2025-09-15T12:00:05Z", LogAnalyzer.DATE_TIME_FORMAT))
        analyzer.generate_report()
        self.assertEquals(analyzer.report_json["total"], 1)
        self.assertNotIn("orders",analyzer.report_json["byService"])
        self.assertEquals(analyzer.report_json["byService"]["billing"], 1)
        self.assertNotIn("alert",analyzer.report_json)




