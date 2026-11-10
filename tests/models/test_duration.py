import unittest

from garminworkouts.models.duration import Duration


class DurationTestCase(unittest.TestCase):
    def test_valid_duration_to_seconds_conversion(self):
        valid_durations = [
            ("0", 0),
            ("10", 10),
            ("10", 10),
            ("59", 59),
            ("0:10", 10),
            ("10:10", 600 + 10),
            ("59:59", 3600 - 1),
            ("0:10:10", 600 + 10),
            ("1:10:10", 3600 + 600 + 10),
            ("23:59:59", 24 * 3600 - 1),
        ]

        for duration, seconds in valid_durations:
            with self.subTest(msg=f"Expected {seconds} seconds for '{duration}'"):
                self.assertEqual(Duration(duration).to_seconds(), seconds)

    def test_invalid_duration_to_seconds_conversion(self):
        invalid_durations = [
            "-1",
            "60",
            "-1:10",
            "60:10",
            "-1:10:10",
            "24:10:10",
            "foo",
            "foo:bar",
            "foo:bar:baz",
            "1:1:1:1",
        ]
        for duration in invalid_durations:
            with self.subTest(msg=f"Expected ValueError for '{duration}"):
                with self.assertRaises(ValueError):
                    Duration(duration).to_seconds()

    def test_invalid_duration_error_names_offending_value(self):
        invalid_durations = [
            ("90:00", "Minutes must be between 0 and 59 but was 90"),
            ("25:10:10", "Hours must be between 0 and 23 but was 25"),
        ]

        for duration, expected_message in invalid_durations:
            with self.subTest(msg=f"Expected message for '{duration}"):
                with self.assertRaises(ValueError) as ctx:
                    Duration(duration).to_seconds()
                self.assertEqual(str(ctx.exception), expected_message)


if __name__ == "__main__":
    unittest.main()
