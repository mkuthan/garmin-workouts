import shutil
from unittest.mock import MagicMock, patch
from garminworkouts.garmin.garminclient import GarminClient
import os


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


def test_export_trainingplans(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'list_trainingplans') as mock_list_trainingplans, \
         patch.object(authed_gclient, 'get_training_plan') as mock_get_training_plan, \
         patch.object(authed_gclient, 'get_workout') as mock_get_workout, \
         patch.object(authed_gclient, 'schedule_training_plan') as mock_schedule_training_plan, \
         patch.object(authed_gclient, 'delete_training_plan') as mock_delete_training_plan:

        mock_list_trainingplans.return_value = [{
            'trainingPlanId': '123',
            'trainingType': {
                'typeKey': 'running'},
            'trainingSubType': {
                'subTypeKey': 'RunningOther'},
            'trainingLevel': {
                'levelKey': 'beginner'},
            'trainingVersion': {
                'versionName': 'Time',
                },
            'name': 'Test Training Plan',
            'description': 'Test Description',
            'durationInWeeks': 12,
            'avgWeeklyWorkouts': 3,
            }]
        mock_schedule_training_plan.return_value = mock_list_trainingplans.return_value[0]
        mock_get_training_plan.return_value = [{
            'weekId': '1',
            'dayOfWeekId': '1',
            'taskWorkout': {
                'workoutId': '123',
                },
            },
            {
            'weekId': '1',
            'dayOfWeekId': '2',
            'taskNote': {
                'note': '123',
                'noteDescription': 'Test Note',
            },
        }]
        mock_get_workout.return_value = MagicMock(json=lambda: {
            'workoutId': '123',
            'name': 'Test Workout',
            'description': 'Test Description',
            'sportType': {
                'sportTypeKey': 'running'},
            })
        mock_delete_training_plan.return_value = MagicMock(status_code=200)
        authed_gclient.export_trainingplans()
        shutil.rmtree(os.path.join('.', 'trainingplans', 'Running', 'Garmin', 'TestTrainingPlan'))


def test_export_trainingplans2(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'list_trainingplans') as mock_list_trainingplans, \
            patch.object(authed_gclient, 'get_training_plan') as mock_get_training_plan, \
            patch.object(authed_gclient, 'get_workout') as mock_get_workout, \
            patch.object(authed_gclient, 'schedule_training_plan') as mock_schedule_training_plan, \
            patch.object(authed_gclient, 'delete_training_plan') as mock_delete_training_plan:

        mock_list_trainingplans.return_value = [{
            'trainingPlanId': '123',
            'trainingType': {
                'typeKey': 'running'},
            'trainingSubType': {
                'subTypeKey': 'EE5k'},
            'trainingLevel': {
                'levelKey': 'beginner'},
            'trainingVersion': {
                'versionName': 'Time',
            },
            'name': 'EE5k',
            'description': 'Test Description',
            'durationInWeeks': 12,
            'avgWeeklyWorkouts': 3,
        }]
        mock_schedule_training_plan.return_value = mock_list_trainingplans.return_value[0]
        mock_get_training_plan.return_value = [{
            'weekId': '1',
            'dayOfWeekId': '1',
            'taskWorkout': {
                'workoutId': '123',
            },
        },
            {
            'weekId': '1',
            'dayOfWeekId': '2',
            'taskNote': {
                'note': '123',
                'noteDescription': 'Test Note',
            },
        }]
        mock_get_workout.return_value = MagicMock(json=lambda: {
            'workoutId': '123',
            'name': 'Test Workout',
            'description': 'Test Description',
            'sportType': {
                'sportTypeKey': 'running'},
        })
        mock_delete_training_plan.return_value = MagicMock(status_code=200)
        authed_gclient.export_trainingplans()
        shutil.rmtree(os.path.join('.', 'trainingplans', 'Running', 'Garmin', 'EE5k'))


def test_external_workout_export_yaml(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'workout_export_yaml') as mock_workout_export_yaml, \
         patch.object(authed_gclient, 'export_trainingplans') as mock_export_trainingplans:
        authed_gclient.external_workout_export_yaml()
        mock_workout_export_yaml.assert_called_once()
        mock_export_trainingplans.assert_called_once()
