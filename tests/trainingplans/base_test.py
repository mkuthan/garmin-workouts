import unittest
import datetime
import argparse
from garminworkouts.models.settings import settings


class BaseTest(unittest.TestCase):
    def check_workout_files(self, tp_list) -> None:
        for tp in tp_list:
            with self.subTest():
                args = argparse.Namespace(trainingplan=tp)
                workouts, notes, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')
