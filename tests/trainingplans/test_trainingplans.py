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
    def test_trainingplan_pfitzinger(self) -> None:
        tp_list: list[str] = [
            os.path.join('fitz*', '5k', '63km', '*.yaml'),
            os.path.join('fitz*', 'base', '72km', '*.yaml'),
            os.path.join('fitz*', 'base', '97km', '*.yaml'),
            os.path.join('fitz*', 'Half', '76km', '*.yaml'),
            os.path.join('fitz*', 'Half', '102km', '*.yaml'),
            os.path.join('fitz*', 'Marathon', '88km', '*', '*.yaml'),
            os.path.join('fitz*', 'Marathon', '113km', '*', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_napier(self) -> None:
        tp_list: list[str] = [
            os.path.join('napier*', 'Marathon', 'Advanced', '*.yaml'),
            os.path.join('napier*', 'Half', 'Advanced', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_5k(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Running', '5k', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Running', '5k', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', 'Running', '5k', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Running', '5k', 'Intermediate', 'HeartRate', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_10k(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Running', '10k', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Running', '10k', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', 'Running', '10k', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Running', '10k', 'Intermediate', 'HeartRate', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_halfmarathon(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Running', 'HalfMarathon', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'HalfMarathon', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'HalfMarathon', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'HalfMarathon', 'Intermediate', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'HalfMarathon', 'Advanced', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'HalfMarathon', 'Advanced', 'HeartRate', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_marathon(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Running', 'Marathon', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'Marathon', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'Marathon', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'Marathon', 'Intermediate', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'Marathon', 'Advanced', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'Marathon', 'Advanced', 'HeartRate', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_runningother(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Running', 'RunningOther', 'Beginner', 'Time', 'GettingStarted',
                         '*.yaml'),
            os.path.join('trainingplans', 'Running', 'RunningOther', 'Beginner', 'HeartRate', 'GettingStarted',
                         '*.yaml'),
            os.path.join('trainingplans', 'Running', 'RunningOther', 'Intermediate', 'Time', 'GettingStarted',
                         '*.yaml'),
            os.path.join('trainingplans', 'Running', 'RunningOther', 'Intermediate', 'HeartRate', 'GettingStarted',
                         '*.yaml'),
            os.path.join('trainingplans', 'Running', 'RunningOther', 'Beginner', 'Time', 'ImproveYourFitness',
                         '*.yaml'),
            os.path.join('trainingplans', 'Running', 'RunningOther', 'Beginner', 'HeartRate',
                         'ImproveYourFitness', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'RunningOther', 'Intermediate', 'Time',
                         'ImproveYourFitness', '*.yaml'),
            os.path.join('trainingplans', 'Running', 'RunningOther', 'Intermediate', 'HeartRate',
                         'ImproveYourFitness', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_triathlonolympic(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Triathlon', 'Olympic', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Triathlon', 'Olympic', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', 'Triathlon', 'Olympic', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Triathlon', 'Olympic', 'Intermediate', 'HeartRate', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_triathlonsprint(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Triathlon', 'Sprint', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Triathlon', 'Sprint', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', 'Triathlon', 'Sprint', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', 'Triathlon', 'Sprint', 'Intermediate', 'HeartRate', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cyclingcrit(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Advanced', 'HeartRate',
                         'RacePhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Advanced', 'Power',
                         'RacePhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Intermediate', 'HeartRate',
                         'RacePhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Intermediate', 'Power',
                         'RacePhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Advanced', 'HeartRate',
                         'RacePhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Advanced', 'Power',
                         'RacePhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Intermediate', 'HeartRate',
                         'RacePhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Intermediate', 'Power',
                         'RacePhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Advanced', 'HeartRate',
                         'RacePhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Advanced', 'Power',
                         'RacePhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Intermediate', 'HeartRate',
                         'RacePhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'Crit', 'Intermediate', 'Power',
                         'RacePhase3Peak', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cyclingfullcentury(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Advanced', 'HeartRate',
                         'CenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Advanced', 'Power',
                         'CenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Intermediate', 'HeartRate',
                         'CenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Intermediate', 'Power',
                         'CenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Advanced', 'HeartRate',
                         'CenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Advanced', 'Power',
                         'CenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Intermediate', 'HeartRate',
                         'CenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Intermediate', 'Power',
                         'CenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Advanced', 'HeartRate',
                         'CenturyPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Advanced', 'Power',
                         'CenturyPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Intermediate', 'HeartRate',
                         'CenturyPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'FullCentury', 'Intermediate', 'Power',
                         'CenturyPhase3Peak', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cyclinggranfondo(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Advanced', 'HeartRate',
                         'GranFondoPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Advanced', 'Power',
                         'GranFondoPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Intermediate', 'HeartRate',
                         'GranFondoPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Intermediate', 'Power',
                         'GranFondoPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Advanced', 'HeartRate',
                         'GranFondoPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Advanced', 'Power',
                         'GranFondoPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Intermediate', 'HeartRate',
                         'GranFondoPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Intermediate', 'Power',
                         'GranFondoPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Advanced', 'HeartRate',
                         'GranFondoPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Advanced', 'Power',
                         'GranFondoPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Intermediate', 'HeartRate',
                         'GranFondoPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'GranFondo', 'Intermediate', 'Power',
                         'GranFondoPhase3Peak', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cyclinghalfcentury(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Cycling', 'HalfCentury', 'Beginner', 'HeartRate',
                         'MetricCenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'HalfCentury', 'Beginner', 'Power',
                         'MetricCenturyPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'HalfCentury', 'Beginner', 'HeartRate',
                         'MetricCenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'HalfCentury', 'Beginner', 'Power',
                         'MetricCenturyPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'HalfCentury', 'Beginner', 'HeartRate',
                         'MetricCenturyPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'HalfCentury', 'Beginner', 'Power',
                         'MetricCenturyPhase3Peak', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_cyclingMTB(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Advanced', 'HeartRate',
                         'MTBPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Advanced', 'Power',
                         'MTBPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Intermediate', 'HeartRate',
                         'MTBPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Intermediate', 'Power',
                         'MTBPhase1Base', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Advanced', 'HeartRate',
                         'MTBPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Advanced', 'Power',
                         'MTBPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Intermediate', 'HeartRate',
                         'MTBPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Intermediate', 'Power',
                         'MTBPhase2Build', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Advanced', 'HeartRate',
                         'MTBPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Advanced', 'Power',
                         'MTBPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Intermediate', 'HeartRate',
                         'MTBPhase3Peak', '*.yaml'),
            os.path.join('trainingplans', 'Cycling', 'MountainBiking', 'Intermediate', 'Power',
                         'MTBPhase3Peak', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_workouts(self) -> None:
        tp_list: list[str] = [
            os.path.join('workouts', 'cardio_training', 'ADVANCED', '*.yaml'),
            os.path.join('workouts', 'cardio_training', 'INTERMEDIATE', '*.yaml'),
            os.path.join('workouts', 'cardio_training', 'BEGINNER', '*.yaml'),
            os.path.join('workouts', 'hiit', 'ADVANCED', '*.yaml'),
            os.path.join('workouts', 'hiit', 'INTERMEDIATE', '*.yaml'),
            os.path.join('workouts', 'hiit', 'BEGINNER', '*.yaml'),
            os.path.join('workouts', 'pilates', 'ADVANCED', '*.yaml'),
            os.path.join('workouts', 'pilates', 'INTERMEDIATE', '*.yaml'),
            os.path.join('workouts', 'pilates', 'BEGINNER', '*.yaml'),
            os.path.join('workouts', 'strength_training', 'ADVANCED', '*.yaml'),
            os.path.join('workouts', 'strength_training', 'INTERMEDIATE', '*.yaml'),
            os.path.join('workouts', 'strength_training', 'BEGINNER', '*.yaml'),
            os.path.join('workouts', 'yoga', 'INTERMEDIATE', '*.yaml'),
            os.path.join('workouts', 'yoga', 'BEGINNER', '*.yaml'),
        ]

        for tp in tp_list:
            with self.subTest():
                args = Arg(trainingplan=tp)
                workouts, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')


if __name__ == '__main__':
    unittest.main()
