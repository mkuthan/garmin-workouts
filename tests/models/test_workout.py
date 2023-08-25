import unittest

from garminworkouts.models.workout import Workout
from tests.test_configs.sample_configurations import workouts
from garminworkouts.garmin.garminclient import GarminClient
import account
import logging


def _garmin_client() -> GarminClient:
    return GarminClient(
        connect_url="https://connect.garmin.com",
        sso_url="https://sso.garmin.com",
        username=account.USERNAME,
        password=account.PASSWORD,
        cookie_jar=".garmin-cookies.txt")


class WorkoutTestCase(unittest.TestCase):
    def test_workout_creation(self) -> None:
        with _garmin_client() as connection:
            existing_workouts_by_name = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

            for workout in workouts:
                with self.subTest(msg="Error for '%s" % workout):
                    workout_name: str = workout.get_workout_name()

                    payload: dict = workout.create_workout()
                    logging.info("Creating workout '%s'", workout_name)
                    connection.save_workout(payload)

                    existing_workouts_by_name: dict = {
                        Workout.extract_workout_name(w): w for w in connection.list_workouts()}
                    existing_workout: Workout | None = existing_workouts_by_name.get(workout_name)

                    workout_id = Workout.extract_workout_id(existing_workout)
                    connection.delete_workout(workout_id)
