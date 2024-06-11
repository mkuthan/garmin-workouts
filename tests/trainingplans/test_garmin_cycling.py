import unittest
import datetime
import os
from garminworkouts.models.settings import settings


class Arg(object):
    def __init__(
        self,
        trainingplan
    ) -> None:
        self.trainingplan = trainingplan


class TrainingPlanTestCase(unittest.TestCase):
    def test_trainingplan_garmin_cycling_crit(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'HeartRate',
                         'RacePhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'Power',
                         'RacePhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'HeartRate',
                         'RacePhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'Power',
                         'RacePhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'HeartRate',
                         'RacePhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'Power',
                         'RacePhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'HeartRate',
                         'RacePhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'Power',
                         'RacePhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'HeartRate',
                         'RacePhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Advanced', 'Power',
                         'RacePhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'HeartRate',
                         'RacePhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Crit', 'Intermediate', 'Power',
                         'RacePhase3Peak', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, notes, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cycling_fullcentury(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'HeartRate',
                         'CenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'Power',
                         'CenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'HeartRate',
                         'CenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'Power',
                         'CenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'HeartRate',
                         'CenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'Power',
                         'CenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'HeartRate',
                         'CenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'Power',
                         'CenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'HeartRate',
                         'CenturyPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Advanced', 'Power',
                         'CenturyPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'HeartRate',
                         'CenturyPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'FullCentury', 'Intermediate', 'Power',
                         'CenturyPhase3Peak', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, notes, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cycling_granfondo(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'HeartRate',
                         'GranFondoPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'Power',
                         'GranFondoPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'HeartRate',
                         'GranFondoPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'Power',
                         'GranFondoPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'HeartRate',
                         'GranFondoPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'Power',
                         'GranFondoPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'HeartRate',
                         'GranFondoPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'Power',
                         'GranFondoPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'HeartRate',
                         'GranFondoPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Advanced', 'Power',
                         'GranFondoPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'HeartRate',
                         'GranFondoPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GranFondo', 'Intermediate', 'Power',
                         'GranFondoPhase3Peak', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, notes, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cycling_halfcentury(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'HeartRate',
                         'MetricCenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'Power',
                         'MetricCenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'HeartRate',
                         'MetricCenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'Power',
                         'MetricCenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'HeartRate',
                         'MetricCenturyPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'HalfCentury', 'Beginner', 'Power',
                         'MetricCenturyPhase3Peak', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, notes, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cycling_MTB(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'HeartRate',
                         'MTBPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'Power',
                         'MTBPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'HeartRate',
                         'MTBPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'Power',
                         'MTBPhase1Base', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'HeartRate',
                         'MTBPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'Power',
                         'MTBPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'HeartRate',
                         'MTBPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'Power',
                         'MTBPhase2Build', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'HeartRate',
                         'MTBPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Advanced', 'Power',
                         'MTBPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'HeartRate',
                         'MTBPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'MountainBiking', 'Intermediate', 'Power',
                         'MTBPhase3Peak', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, notes, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')
