from datetime import date
import unittest
from unittest.mock import patch
from garminworkouts.models.settings import planning_workout_files, settings
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

        workouts, notes, events, plan = settings(args, defaultPlanning=defaultPlanning)
        self.assertEqual(len(workouts), 37)
        self.assertEqual(len(notes), 47)
        self.assertEqual(len(events), 0)
        self.assertEqual(plan, 'tp')

    def test_settings_positive(self) -> None:
        args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

        workouts, notes, events, plan = settings(args)
        self.assertEqual(len(workouts), 37)
        self.assertEqual(len(notes), 47)
        self.assertEqual(len(events), 0)
        self.assertEqual(plan, '')

    def test_settings_negative(self) -> None:
        args = argparse.Namespace(trainingplan='non_existent_plan')
        with patch('garminworkouts.config.configreader.read_config') as mock_read_config:
            mock_read_config.return_value = {}
            workouts, notes, events, plan = settings(args)
            self.assertEqual(len(workouts), 0)
            self.assertEqual(len(notes), 0)
            self.assertEqual(len(events), 0)
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
            workouts, notes, events, plan = settings(args, defaultPlanning)
            self.assertEqual(len(workouts), 0)
            self.assertEqual(len(notes), 0)
            self.assertEqual(len(events), 0)
            self.assertEqual(plan, '')

    def test_settings_event(self) -> None:
        defaultPlanning: dict = {
            'tp': {
                'workouts': 'events/planning/sample_event.yaml',
                'year': 2024,
                'month': 1,
                'day': 1
            }
        }
        args = argparse.Namespace(trainingplan='tp')
        workouts, notes, events, plan = settings(args, defaultPlanning=defaultPlanning)
        self.assertEqual(len(workouts), 1)
        self.assertEqual(len(notes), 0)
        self.assertEqual(len(events), 1)
        self.assertEqual(plan, 'tp')

    def test_planning_workout_files_with_default_planning(self) -> None:
        args = argparse.Namespace(trainingplan='tp')

        defaultPlanning: dict = {
            'tp': {
                'workouts': ['trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml'],
                'year': 2024,
                'month': 1,
                'day': 1
                }
            }

        workout_files, race, plan = planning_workout_files(args, defaultPlanning=defaultPlanning)
        self.assertTrue(len(workout_files) > 0)
        self.assertEqual(race, date(2024, 1, 1))
        self.assertEqual(plan, 'tp')

    def test_planning_workout_files_with_yaml_trainingplan(self) -> None:
        args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

        workout_files, race, plan = planning_workout_files(args)
        self.assertTrue(len(workout_files) > 0)
        self.assertEqual(race, date.today())
        self.assertEqual(plan, '')

    def test_planning_workout_files_with_non_existent_plan(self) -> None:
        args = argparse.Namespace(trainingplan='non_existent_plan')
        with patch('garminworkouts.config.configreader.read_config') as mock_read_config:
            mock_read_config.return_value = {}
            workout_files, race, plan = planning_workout_files(args)
            self.assertEqual(len(workout_files), 0)
            self.assertEqual(race, date.today())
            self.assertEqual(plan, '')

    def test_planning_workout_files_file_not_found(self) -> None:
        args = argparse.Namespace(trainingplan='tp')
        with patch('garminworkouts.config.configreader.read_config') as mock_read_config:
            mock_read_config.side_effect = FileNotFoundError
            workout_files, race, plan = planning_workout_files(args)
            self.assertEqual(len(workout_files), 0)
            self.assertEqual(race, date.today())
            self.assertEqual(plan, '')

    def test_planning_workout_files_event(self) -> None:
        defaultPlanning: dict = {
            'tp': {
                'workouts': 'events/planning/sample_event.yaml',
                'year': 2024,
                'month': 1,
                'day': 1
                }
            }
        args = argparse.Namespace(trainingplan='tp')
        workout_files, race, plan = planning_workout_files(args, defaultPlanning=defaultPlanning)
        self.assertTrue(len(workout_files) > 0)
        self.assertEqual(race, date(2024, 1, 1))
        self.assertEqual(plan, 'tp')
