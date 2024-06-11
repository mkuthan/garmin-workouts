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
                workouts, notes, plan = settings(args)
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
                workouts, notes, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')
