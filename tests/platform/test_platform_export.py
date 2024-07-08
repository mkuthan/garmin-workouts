import shutil
from unittest.mock import patch
from garminworkouts.garmin.garminclient import GarminClient


def test_export_external_workouts(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'external_workouts') as mock_external_workouts, \
         patch.object(authed_gclient, 'get_external_workout') as mock_get_external_workout:
        mock_external_workouts.return_value = [{
            'workoutSourceId': '123',
            'sportTypeKey': 'running',
            'difficulty': 'Beginner'}]
        mock_get_external_workout.return_value = {
            'workoutId': '123',
            'name': 'Test Workout',
            'sportType': {
                'sportTypeKey': 'running',
            },
            'description': 'Test Description',
            }
        authed_gclient.workout_export_yaml()
        shutil.rmtree('./workouts/running/Beginner')
