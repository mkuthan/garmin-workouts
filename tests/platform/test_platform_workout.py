from garminworkouts.garmin.garminclient import GarminClient
from tests.trainingplans.base_test import BaseTest
import os


def test_external_workouts(authed_gclient: GarminClient) -> None:
    locale = 'en-US'
    workout_list: dict = authed_gclient.external_workouts(locale)
    assert workout_list


def test_get_external_workout(authed_gclient: GarminClient) -> None:
    locale = 'en-US'
    workouts: dict = authed_gclient.external_workouts(locale)

    for workout in workouts:
        w: dict = authed_gclient.get_external_workout(workout['workoutSourceId'], locale)
        assert w


def test_list_workouts(authed_gclient: GarminClient) -> None:
    # Call the method under test
    workouts = list(authed_gclient.list_workouts())

    # Assert that the returned value is a list
    assert isinstance(workouts, list)

    # Assert that the list is not empty
    assert len(workouts) > 0

    # Assert that each item in the list is a dictionary
    assert all(isinstance(workout, dict) for workout in workouts)


class WorkoutestCase(BaseTest):
    def test_workout(self) -> None:
        workout_files: list = [
            os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1', '21_1.yaml'),
            os.path.join('.', 'trainingplans', 'Running', '*', '5k', 'Beginner', 'Time', 'R1_1.yaml')
        ]
        self.platform_workout_files(workout_files)
