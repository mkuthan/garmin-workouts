from requests import Response
from garminworkouts.garmin.garminclient import GarminClient
from tests.trainingplans.base_test import BaseTest
import os
from unittest.mock import patch


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

    # Assert that the list is created
    assert len(workouts) >= 0

    # Assert that each item in the list is a dictionary
    assert all(isinstance(workout, dict) for workout in workouts)


def test_get_note(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        note_id = 123
        mock_get.return_value = [{'uuid': '123', 'note': 'Sample note'}]
        note: Response = authed_gclient.get_note(True, note_id)
        mock_get.assert_called_once_with(f"{GarminClient._TRAINING_PLAN_SERVICE_ENDPOINT}/scheduled/notes/{note_id}")

        assert note


class WorkoutTestCase(BaseTest):
    def test_workout(self) -> None:
        workout_files: list = [
            os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1', '21_1.yaml'),
            os.path.join('.', 'trainingplans', 'Running', '*', '5k', 'Beginner', 'Time', 'R1_1.yaml')
        ]
        self.platform_workout_files(workout_files)


def test_generate_filename_with_a_in_ww(authed_gclient: GarminClient) -> None:
    newpath = ''
    name = 'R1_1'
    ww = 'W01D01a -'
    expected_filename = 'R1_1a.yaml'

    filename: str = authed_gclient.generate_filename(newpath, name, ww)
    assert filename == expected_filename


def test_generate_filename_with_b_in_ww(authed_gclient: GarminClient) -> None:
    newpath = ''
    name = 'R2_2'
    ww = 'W02D02b -'
    expected_filename = 'R2_2b.yaml'

    filename: str = authed_gclient.generate_filename(newpath, name, ww)

    assert filename == expected_filename


def test_generate_filename_without_a_or_b_in_ww(authed_gclient: GarminClient) -> None:
    newpath = ''
    name = 'R3_3'
    ww = 'Workout'
    expected_filename = 'R3_3.yaml'

    filename: str = authed_gclient.generate_filename(newpath, name, ww)

    assert filename == expected_filename
