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
                workouts, notes, plan = settings(args)
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
                workouts, notes, plan = settings(args)
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
                workouts, notes, plan = settings(args)
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
                workouts, notes, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_garmin_runningother(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', '*', '*', 'GettingStarted', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GettingStarted', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GettingStarted', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'GettingStarted', 'Intermediate', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'ImproveYourFitness', 'Beginner', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'ImproveYourFitness', 'Beginner', 'HeartRate', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'ImproveYourFitness', 'Intermediate', 'Time', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'ImproveYourFitness', 'Intermediate', 'HeartRate', '*.yaml'),
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
