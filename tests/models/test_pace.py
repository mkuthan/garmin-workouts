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

    def test_to_pace_percent(self) -> None:
        pace = Pace('50%')
        self.assertEqual(pace.to_pace(), 2.7777777777777777)

    def test_to_pace_absolute(self) -> None:
        pace = Pace('3:00')
        self.assertEqual(pace.to_pace('3:00', 0), 5.555555555555555)

    def test_has_time_true(self) -> None:
        pace = Pace('5:30')
        self.assertTrue(pace._has_time())

    def test_has_time_false(self) -> None:
        pace = Pace('50%')
        self.assertFalse(pace._has_time())

    def test_has_percent_true(self) -> None:
        pace = Pace('50%')
        self.assertTrue(pace._has_percent())

    def test_has_percent_false(self) -> None:
        pace = Pace('5:30')
        self.assertFalse(pace._has_percent())

    def test_to_absolute(self) -> None:
        self.assertEqual(Pace._to_absolute(3, 50), 1.5)


if __name__ == '__main__':
    unittest.main()
