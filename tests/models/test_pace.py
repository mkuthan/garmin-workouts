import unittest
from garminworkouts.models.pace import Pace


class TestPace(unittest.TestCase):

    def test_to_seconds_positive(self) -> None:
        pace = Pace('5:30')
        self.assertEqual(pace.to_seconds(), 330)

    def test_to_speed(self) -> None:
        pace = Pace('5:30')
        self.assertEqual(pace.to_speed(), 3.0303030303030303)

    def test_to_pace_time(self) -> None:
        pace = Pace('5:30')
        self.assertEqual(pace.to_pace(), 3.0303030303030303)

    def test_to_pace_absolute(self) -> None:
        pace = Pace('3:00')
        self.assertEqual(pace.to_pace('3:00', 0), 5.555555555555555)

    def test_has_time_true(self) -> None:
        pace = Pace('5:30')
        self.assertTrue(pace._has_time())

    def test_has_time_false(self) -> None:
        pace = Pace('50%')
        self.assertFalse(pace._has_time())

    def test_to_absolute(self) -> None:
        self.assertEqual(Pace._to_absolute(3, 50), 1.5)

    def test_to_pace(self) -> None:
        pace = Pace('5:30')
        self.assertEqual(pace.to_pace(), 3.0303030303030303)

    def test_to_pace_error(self) -> None:
        pace = Pace('0')
        with self.assertRaises(ValueError):
            pace.to_pace('5:00')

    def test_to_pace_with_vVO2(self) -> None:
        pace = Pace('5:30')
        self.assertEqual(pace.to_pace('3:00'), 3.0303030303030303)
        with self.assertRaises(ValueError):
            pace.to_pace('59:00')

    def test_to_pace_with_diff(self) -> None:
        pace = Pace('5:30')
        self.assertEqual(pace.to_pace(diff=500), 1.2048192771084336)

    def test_to_pace_with_vVO2_and_diff(self) -> None:
        pace = Pace('5:30')
        self.assertEqual(pace.to_pace('3:00', 500), 1.2048192771084336)
