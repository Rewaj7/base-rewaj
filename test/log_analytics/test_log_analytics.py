import unittest
from datetime import datetime

from log_analytics.analyzer import LogAnalyzer


class TestLogAnalyzer(unittest.TestCase):

    def test_init(self):
        analyzer = LogAnalyzer("rewaj-cb-tf", "base_json/2025-09-15T12-00.jsonl", 5)
        self.assertEquals(analyzer.s3_reader.bucket_name, "rewaj-cb-tf")
        self.assertTrue(analyzer.s3_reader.file_directory, "base_json/2025-09-15T12-00.jsonl")
        analyzer.close()


    def test_get_next_json_line(self):
        analyzer = LogAnalyzer("rewaj-cb-tf", "base_json/2025-09-15T12-00.jsonl", 5)
        first_json_line = analyzer.get_next_json_line()
        self.assertEquals(first_json_line["service"], "orders")
        self.assertEquals(first_json_line["msg"], "new order received")

        second_json_line = analyzer.get_next_json_line()
        self.assertEquals(second_json_line["service"], "orders")
        self.assertEquals(second_json_line["msg"], "payment declined")

        analyzer.close()

    def test_is_next_line_error(self):
        analyzer = LogAnalyzer("rewaj-cb-tf", "base_json/2025-09-15T12-00.jsonl", 5)
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
        analyzer = LogAnalyzer("rewaj-cb-tf", "base_json/2025-09-15T12-00.jsonl", 5)
        analyzer.generate_report()
        number_of_errors = analyzer.report_json
        self.assertEquals(number_of_errors["total"], 2)
        self.assertEquals(number_of_errors["byService"]["orders"], 1)
        self.assertEquals(number_of_errors["byService"]["billing"], 1)
        self.assertNotIn("api",number_of_errors["byService"])

    def test_alert_threshold(self):
        high_threshold = LogAnalyzer("rewaj-cb-tf", "base_json/2025-09-15T12-00.jsonl", 5)
        high_threshold.generate_report()
        high_threshold_json = high_threshold.report_json
        self.assertNotIn("alert",high_threshold_json)

        low_threshold = LogAnalyzer("rewaj-cb-tf", "base_json/2025-09-15T12-00.jsonl", 2)
        low_threshold.generate_report()
        low_threshold_json = low_threshold.report_json
        self.assertEquals("true",low_threshold_json["alert"])

    def test_number_of_errors_with_since(self):
        analyzer = LogAnalyzer("rewaj-cb-tf",
                               "base_json/2025-09-15T12-00.jsonl",
                               2,
                               time_stamp=datetime.strptime("2025-09-15T12:00:05Z", LogAnalyzer.DATE_TIME_FORMAT))
        analyzer.generate_report()
        self.assertEquals(analyzer.report_json["total"], 1)
        self.assertNotIn("orders",analyzer.report_json["byService"])
        self.assertEquals(analyzer.report_json["byService"]["billing"], 1)
        self.assertNotIn("alert",analyzer.report_json)




