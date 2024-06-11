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
                workouts, notes, plan = settings(args)
                self.assertGreater(len(workouts), 0, tp + ' has not files')

                for workout in workouts:
                    self.assertNotEqual(
                        workout.duration == datetime.timedelta(seconds=0) and workout.mileage == 0,
                        True,
                        msg=tp + ' ' + workout.config['name'] + ' drops an exception')

    def test_trainingplan_darebee(self) -> None:
        tp_list: list[str] = [
            os.path.join('trainingplans', 'Strength', 'Darebee', 'Challenges', '3-normal', '1-minute plank', '*.yaml'),
            os.path.join('trainingplans', 'Strength', 'Darebee', 'Challenges', '3-normal', 'first thing plank hold',
                         '*.yaml'),
            os.path.join('trainingplans', 'Strength', 'Darebee', 'Challenges', '3-normal', 'the miner', '*.yaml'),
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


if __name__ == '__main__':
    unittest.main()
