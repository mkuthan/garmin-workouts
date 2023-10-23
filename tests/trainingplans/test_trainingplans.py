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
            os.path.join('trainingplans', '*', '*', '5k', '63km', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'base', '72km', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'base', '97km', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Half', '76km', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Half', '102km', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', '88km', '*', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', '113km', '*', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', '113km-12w', '*', '*.yaml'),
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
            os.path.join('trainingplans', '*', '*', 'Marathon', 'Advanced', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Half', 'Advanced', '*.yaml'),
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
            os.path.join('trainingplans', '*', '*', '5k', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', '5k', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', '5k', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', '5k', 'Intermediate', 'HeartRate', '*.yaml'),
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
            os.path.join('trainingplans', '*', '*', '10k', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', '10k', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', '10k', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', '10k', 'Intermediate', 'HeartRate', '*.yaml'),
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
            os.path.join('trainingplans', '*', '*', 'HalfMarathon', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'HalfMarathon', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'HalfMarathon', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'HalfMarathon', 'Intermediate', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'HalfMarathon', 'Advanced', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'HalfMarathon', 'Advanced', 'HeartRate', '*.yaml'),
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
            os.path.join('trainingplans', '*', '*', 'Marathon', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', 'Intermediate', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', 'Advanced', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', 'Advanced', 'HeartRate', '*.yaml'),
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
            os.path.join('trainingplans', '*', '*', 'RunningOther', 'Beginner', 'Time', 'GettingStarted',
                         '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'RunningOther', 'Beginner', 'HeartRate', 'GettingStarted',
                         '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'RunningOther', 'Intermediate', 'Time', 'GettingStarted',
                         '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'RunningOther', 'Intermediate', 'HeartRate', 'GettingStarted',
                         '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'RunningOther', 'Beginner', 'Time', 'ImproveYourFitness',
                         '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'RunningOther', 'Beginner', 'HeartRate',
                         'ImproveYourFitness', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'RunningOther', 'Intermediate', 'Time',
                         'ImproveYourFitness', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'RunningOther', 'Intermediate', 'HeartRate',
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
            os.path.join('trainingplans', '*', '*', 'Olympic', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Olympic', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Olympic', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Olympic', 'Intermediate', 'HeartRate', '*.yaml'),
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
            os.path.join('trainingplans', '*', '*', 'Sprint', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Sprint', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Sprint', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Sprint', 'Intermediate', 'HeartRate', '*.yaml'),
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
                workouts, plan = settings(args)
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
                workouts, plan = settings(args)
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
                workouts, plan = settings(args)
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
                workouts, plan = settings(args)
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

    def test_trainingplan_nike_marathon(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Running', 'Nike', 'Marathon', '*.yaml'),
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
