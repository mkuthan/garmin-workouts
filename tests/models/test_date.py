import unittest
from datetime import date
from garminworkouts.models.date import get_date


class TestGetDate(unittest.TestCase):

    def test_get_date_with_R(self) -> None:
        name = 'R1_3'
        race = date(2022, 1, 1)
        expected_output: tuple[date, int, int] = (date(2022, 1, 4), -1, 3)
        self.assertEqual(get_date(name, race), expected_output)

    def test_get_date_without_R(self) -> None:
        name = '1_3'
        race = date(2022, 1, 1)
        expected_output: tuple[date, int, int] = (date(2021, 12, 21), 1, 3)
        self.assertEqual(get_date(name, race), expected_output)

    def test_get_date_without(self) -> None:
        name = 'SampleNote'
        race = date(2022, 1, 1)
        expected_output: tuple[date, int, int] = (date.today(), 0, 0)
        self.assertEqual(get_date(name, race), expected_output)


if __name__ == '__main__':
    unittest.main()
