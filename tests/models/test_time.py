import unittest
from garminworkouts.models.time import Time


class TestTime(unittest.TestCase):

    def test_to_seconds_positive(self) -> None:
        t = Time("01:30:45")
        self.assertEqual(t.to_seconds(), 5445)

    def test_to_seconds_negative(self) -> None:
        t = Time("00:00:00")
        self.assertEqual(t.to_seconds(), 0)

    def test_to_str_positive(self) -> None:
        self.assertEqual(Time.to_str(3661), "1:01:01")

    def test_to_str_negative(self) -> None:
        self.assertNotEqual(Time.to_str(3600), "1:00:01")
