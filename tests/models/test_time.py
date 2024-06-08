import unittest
from garminworkouts.models.time import Time


class TestTime(unittest.TestCase):

    def test_to_seconds_positive(self):
        t = Time("01:30:45")
        self.assertEqual(t.to_seconds(), 5445)

    def test_to_seconds_negative(self):
        t = Time("00:00:00")
        self.assertEqual(t.to_seconds(), 0)

    def test_to_str_positive(self):
        self.assertEqual(Time.to_str(3661), "1:01:01")

    def test_to_str_negative(self):
        self.assertNotEqual(Time.to_str(3600), "1:00:01")


if __name__ == '__main__':
    unittest.main()
