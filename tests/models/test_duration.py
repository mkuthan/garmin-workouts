import unittest

from garminworkouts.models.duration import Duration


class DurationTestCase(unittest.TestCase):
    def test_valid_duration_to_seconds_conversion(self) -> None:
        valid_durations: list = [
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

    def test_invalid_duration_to_seconds_conversion(self) -> None:
        invalid_durations: list[str] = ["-1", "60", "-1:10", "60:10", "-1:10:10", "24:10:10", "foo", "foo:bar",
                                        "foo:bar:baz", "1:1:1:1"]
        for duration in invalid_durations:
            with self.subTest(msg="Expected ValueError for '%s" % duration):
                with self.assertRaises(ValueError):
                    Duration(duration).to_seconds()

    def test_get_type(self) -> None:
        duration = Duration('5km')
        self.assertEqual(duration.get_type(), 'distance')

        duration = Duration('30:00')
        self.assertEqual(duration.get_type(), 'time')

        duration = Duration('10reps')
        self.assertEqual(duration.get_type(), 'reps')

        duration = Duration('150ppm')
        self.assertEqual(duration.get_type(), 'heart.rate')

        duration = Duration('50cals')
        self.assertEqual(duration.get_type(), 'calories')

        duration = Duration('200w')
        self.assertEqual(duration.get_type(), 'power')

        duration = Duration('lap.button')
        self.assertEqual(duration.get_type(), 'lap.button')

    def test_get_string(self) -> None:
        self.assertEqual(Duration.get_string(100, 'distance'), '100m')
        self.assertEqual(Duration.get_string(150, 'distance'), '150m')
        self.assertEqual(Duration.get_string(200, 'distance'), '200m')
        self.assertEqual(Duration.get_string(2, 'distance'), '2km')
        self.assertEqual(Duration.get_string(50, 'heart.rate'), '50ppm')
        self.assertEqual(Duration.get_string(30, 'time'), '0:00:30')
        self.assertEqual(Duration.get_string(10, 'reps'), '10reps')
        self.assertEqual(Duration.get_string(200, 'power'), '200w')
        self.assertEqual(Duration.get_string(50, 'calories'), '50cals')
        self.assertEqual(Duration.get_string(50, 'invalid'), '')

    def test_get_value(self) -> None:
        self.assertEqual(Duration.get_value('5km'), 5)
        self.assertEqual(Duration.get_value('30:00'), 1800)
        self.assertEqual(Duration.get_value('10reps'), 10)
        self.assertEqual(Duration.get_value('150ppm'), 150)
        self.assertEqual(Duration.get_value('50cals'), 50)
        self.assertEqual(Duration.get_value('200w'), 200)
        self.assertEqual(Duration.get_value('invalid'), None)

    def test_is_time(self) -> None:
        self.assertEqual(Duration.is_time('30:00'), True)
        self.assertEqual(Duration.is_time('5km'), False)

    def test_is_distance(self) -> None:
        self.assertEqual(Duration.is_distance('5km'), True)
        self.assertEqual(Duration.is_distance('150m'), True)
        self.assertEqual(Duration.is_distance('10reps'), False)

    def test_is_reps(self) -> None:
        self.assertEqual(Duration.is_reps('10reps'), True)
        self.assertEqual(Duration.is_reps('5km'), False)

    def test_is_heart_rate(self) -> None:
        self.assertEqual(Duration.is_heart_rate('150ppm'), True)
        self.assertEqual(Duration.is_heart_rate('5km'), False)

    def test_is_power(self) -> None:
        self.assertEqual(Duration.is_power('200w'), True)
        self.assertEqual(Duration.is_power('5km'), False)

    def test_is_energy(self) -> None:
        self.assertEqual(Duration.is_energy('50cals'), True)
        self.assertEqual(Duration.is_energy('5km'), False)

    def test_to_seconds(self) -> None:
        duration = Duration('30:00')
        self.assertEqual(duration.to_seconds(), 1800)

        duration = Duration('1:30:00')
        self.assertEqual(duration.to_seconds(), 5400)


if __name__ == '__main__':
    unittest.main()
