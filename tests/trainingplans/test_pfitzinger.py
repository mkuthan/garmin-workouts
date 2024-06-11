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
            os.path.join('trainingplans', '*', '*', '5k', '111km', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'base', '72km', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'base', '97km', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Half', '76km', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Half', '102km', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', '88km', '*', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', '113km', '*', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', '113km-12w', '*', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', 'Mult-4w', '*', '*.yaml'),
            os.path.join('trainingplans', '*', '*', 'Marathon', 'Mult-8w', '*', '*.yaml'),
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
