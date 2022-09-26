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
            ("23:59:59", 24 * 3600 - 1)
        ]

        for duration, seconds in valid_durations:
            with self.subTest(msg="Expected %d seconds for '%s'" % (seconds, duration)):
                self.assertEqual(Duration(duration).to_seconds(), seconds)

    def test_invalid_duration_to_seconds_conversion(self):
        invalid_durations = ["-1", "60", "-1:10", "60:10", "-1:10:10", "24:10:10", "foo", "foo:bar", "foo:bar:baz",
                             "1:1:1:1"]
        for duration in invalid_durations:
            with self.subTest(msg="Expected ValueError for '%s" % duration):
                with self.assertRaises(ValueError):
                    Duration(duration).to_seconds()


if __name__ == '__main__':
    unittest.main()
