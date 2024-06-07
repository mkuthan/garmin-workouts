import unittest
from unittest.mock import patch
from garminworkouts.models.settings import settings
import argparse


class TestSettingsFunction(unittest.TestCase):
    def test_settings_positive(self) -> None:
        args = argparse.Namespace(trainingplan='my_training_plan')
        with patch('garminworkouts.config.configreader.read_config') as mock_read_config:
            mock_read_config.return_value = {'my_training_plan': {'workouts': 'workout.yaml'}}
            with patch('glob.glob') as mock_glob:
                mock_glob.return_value = ['workout.yaml']

                workouts, notes, plan = settings(args)
                self.assertEqual(len(workouts), 1)
                self.assertEqual(len(notes), 0)
                self.assertEqual(plan, 'my_training_plan')

    def test_settings_negative(self) -> None:
        args = argparse.Namespace(trainingplan='non_existent_plan')
        with patch('garminworkouts.config.configreader.read_config') as mock_read_config:
            mock_read_config.return_value = {}
            workouts, notes, plan = settings(args)
            self.assertEqual(len(workouts), 0)
            self.assertEqual(len(notes), 0)
            self.assertEqual(plan, '')


if __name__ == '__main__':
    unittest.main()
