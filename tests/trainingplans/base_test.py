import unittest
import os
from datetime import date
import datetime
import argparse
import account
from requests import Response
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.settings import settings
from garminworkouts.models.workout import Workout


class BaseTest(unittest.TestCase):
    def check_workout_files(self, tp_list) -> None:
        authed_gclient = GarminClient(account.EMAIL, account.PASSWORD)
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
                    payload: dict = workout.create_workout()
                    self.assertIsInstance(payload, dict, tp + ' ' + workout.config['name'] + ' drops an exception')
                    w: dict = authed_gclient.save_workout(payload)
                    self.assertIsInstance(w, dict,  tp + ' ' + workout.config['name'] + ' drops an exception')
                    workout_id: str = Workout.extract_workout_id(w)
                    self.assertIsInstance(workout_id, (int, float),     tp + ' ' + workout.config['name']
                                          + ' drops an exception')
                    self.assertNotIsInstance(workout_id, bool)
                    payload = workout.create_workout(workout_id=workout_id)
                    self.assertIsInstance(payload, dict)
                    r: Response = authed_gclient.update_workout(workout_id, payload)
                    self.assertIsInstance(r, Response)
                    self.assertIn(r.status_code, (200, 204))
                    r = authed_gclient.get_workout(workout_id)
                    self.assertIsInstance(r, Response)
                    self.assertIn(r.status_code, (200, 204))
                    self.assertIsInstance(authed_gclient.download_workout(workout_id, f"{workout_id}.fit"), bytes)
                    os.remove(f"{workout_id}.fit")
                    self.assertIsInstance(authed_gclient.download_workout_yaml(workout_id, f"{workout_id}.yaml"), dict)
                    os.remove(f"{workout_id}.yaml")
                    p: dict = authed_gclient.schedule_workout(workout_id, date.today().isoformat())
                    r = authed_gclient.remove_workout(p['workoutScheduleId'], date.today().isoformat())
                    self.assertIsInstance(r, Response)
                    self.assertIn(r.status_code, (200, 204))
                    r = authed_gclient.delete_workout(workout_id)
                    self.assertIsInstance(r, Response)
                    self.assertIn(r.status_code, (200, 204))
