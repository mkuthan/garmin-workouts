import unittest
from unittest.mock import patch
from garminworkouts.models.settings import settings
import argparse


class TestSettingsFunction(unittest.TestCase):
    def test_settings(self) -> None:
        args = argparse.Namespace(trainingplan='tp')

        defaultPlanning: dict = {
            'tp': {
                'workouts': ['trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml'],
                'year': 2024,
                'month': 1,
                'day': 1
            }
        }

        workouts, notes, plan = settings(args, defaultPlanning=defaultPlanning)
        self.assertEqual(len(workouts), 37)
        self.assertEqual(len(notes), 47)
        self.assertEqual(plan, 'tp')

    def test_settings_positive(self) -> None:
        args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

        workouts, notes, plan = settings(args)
        self.assertEqual(len(workouts), 37)
        self.assertEqual(len(notes), 47)
        self.assertEqual(plan, '')

    def test_settings_negative(self) -> None:
        args = argparse.Namespace(trainingplan='non_existent_plan')
        with patch('garminworkouts.config.configreader.read_config') as mock_read_config:
            mock_read_config.return_value = {}
            workouts, notes, plan = settings(args)
            self.assertEqual(len(workouts), 0)
            self.assertEqual(len(notes), 0)
            self.assertEqual(plan, '')

    def test_settings_file_not_found(self) -> None:
        defaultPlanning: dict = {
            'tp': {
                'workouts': 'trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml',
                'year': 2024,
                'month': 1,
                'day': 1
            }
        }
        args = argparse.Namespace(trainingplan='tp')
        with patch('garminworkouts.config.configreader.read_config') as mock_read_config:
            mock_read_config.side_effect = FileNotFoundError
            workouts, notes, plan = settings(args, defaultPlanning)
            self.assertEqual(len(workouts), 0)
            self.assertEqual(len(notes), 0)
            self.assertEqual(plan, '')
