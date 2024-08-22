import unittest
from datetime import date
from garminworkouts.models.date import get_date


class TestGetDate(unittest.TestCase):

    def test_get_date_with_R(self) -> None:
        name = 'R1_3'
        race = date(2022, 1, 1)
        expected_output: tuple[date, int, int] = (date(2022, 1, 4), -1, 3)
        self.assertEqual(get_date(name, race, None), expected_output)

    def test_get_date_without_R(self) -> None:
        name = '1_3'
        race = date(2022, 1, 1)
        expected_output: tuple[date, int, int] = (date(2021, 12, 21), 1, 3)
        self.assertEqual(get_date(name, race, None), expected_output)

    def test_get_date_without(self) -> None:
        name = 'SampleNote'
        race = date(2022, 1, 1)
        expected_output: tuple[date, int, int] = (date.today(), 0, 0)
        self.assertEqual(get_date(name, race, None), expected_output)

    def test_get_date_with_negative_week(self) -> None:
        name = 'R2_1'
        race = date(2022, 1, 1)
        expected_output: tuple[date, int, int] = (date(2022, 1, 9), -2, 1)
        self.assertEqual(get_date(name, race, None), expected_output)

    def test_get_date_with_date_ini(self) -> None:
        name = 'Sample'
        race = date(2022, 1, 1)
        date_ini: dict[str, int] = {'year': 2023, 'month': 2, 'day': 15}
        expected_output: tuple[date, int, int] = (date(2023, 2, 15), 0, 0)
        self.assertEqual(get_date(name, race, date_ini), expected_output)
