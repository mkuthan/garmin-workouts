import argparse
from unittest.mock import patch
from datetime import date
from requests import Response
from garminworkouts.garmin.garminclient import GarminClient
from unittest import mock


def test_trainingplan_methods(authed_gclient: GarminClient) -> None:
    tp_list: dict = authed_gclient.list_trainingplans(locale='en-US')
    assert tp_list
    tp: dict = tp_list[0]
    tp_s: dict = authed_gclient.schedule_training_plan(plan_id=tp['trainingPlanId'], startDate=date.today().isoformat())
    assert tp_s
    tp = authed_gclient.get_training_plan(plan_id=tp['trainingPlanId'])
    assert tp
    r: Response = authed_gclient.delete_training_plan(plan_id=tp_s['trainingPlanId'])
    assert r


def test_trainingplan_reset_existing_workout(authed_gclient: GarminClient) -> None:
    args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

    with patch.object(authed_gclient, 'list_workouts') as mock_list_workouts:
        mock_list_workouts.return_value = [{
            "workoutName": "W10D2-Intervals",
            "description": "Intervals",
            }]
        with patch.object(authed_gclient, 'delete_workout') as mock_delete_workout:
            authed_gclient.trainingplan_reset(args)
            assert mock_list_workouts.call_count == 1
            assert mock_delete_workout.call_count == 1


@mock.patch('garminworkouts.garmin.garmintrainingplan.GarminTrainingplan.delete')
def test_delete_training_plan_workout(mock_delete, authed_gclient: GarminClient) -> None:
    # Mock the delete method
    mock_delete.return_value = Response()

    # Call the delete_training_plan_workout method
    result: Response = authed_gclient.delete_training_plan_workout(plan_id='plan_id', workout_id='workout_id')

    # Assert that the delete method was called with the correct arguments
    mock_delete.assert_called_once_with('/trainingplan-service/trainingplan/workoutTask/plan_id/workout_id')

    # Assert that the result is an instance of Response
    assert isinstance(result, Response)
