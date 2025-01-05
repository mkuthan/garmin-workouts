import argparse
from unittest import mock

import pytest
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.__main__ import (_garmin_client, command_event_get, command_event_import, command_find_events,
                                     command_trainingplan_import, command_trainingplan_metrics, command_user_zones,
                                     command_workout_delete, command_workout_export, command_workout_export_yaml,
                                     command_workout_get, command_workout_schedule, update_garmin,
                                     command_update_types, command_trainingplan_reset,
                                     command_activity_list, command_trainingplan_list, command_challenge_list,
                                     command_workout_list, command_event_list)
from garminworkouts.models.event import Event
from garminworkouts.models.workout import Workout


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_workout_list(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_workout_list(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_event_list(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_event_list(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_find_events(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    with mock.patch.object(authed_gclient, '_find_events') as mock_command_user_zones:
        mock_command_user_zones.return_value = None
        assert command_find_events(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_user_zones(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    with mock.patch.object(authed_gclient, 'user_zones') as mock_command_user_zones:
        mock_command_user_zones.return_value = None
        assert command_user_zones(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_workout_export_yaml(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    with mock.patch.object(authed_gclient, 'user_zones') as mock_command_workout_export_yaml:
        mock_command_workout_export_yaml.return_value = None
        assert mock_command_workout_export_yaml(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_challenge_list(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_challenge_list(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_trainingplan_list(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_trainingplan_list(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_activity_list(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_activity_list(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_update_types(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_update_types(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_update_garmin(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert update_garmin(None) is None


@mock.patch('garminworkouts.garmin.garminclient.GarminClient')
def test__garmin_client(mock_garmin_client) -> None:
    # Mock the GarminClient class
    mock_garmin_client.return_value.__enter__.return_value = mock_garmin_client

    # Call the _garmin_client function
    result: GarminClient = _garmin_client()

    # Assert that the result is an instance of GarminClient
    assert isinstance(result, GarminClient)


@mock.patch('garminworkouts.__main__.account')
@mock.patch('garminworkouts.garmin.garminclient.GarminClient')
def test__garmin_client_success(mock_garmin_client, mock_account) -> None:
    # Mock the account module's EMAIL and PASSWORD
    mock_account.EMAIL = 'test@example.com'
    mock_account.PASSWORD = 'password123'

    # Mock the GarminClient class
    mock_garmin_client.return_value.__enter__.return_value = mock_garmin_client

    # Call the _garmin_client function
    result: GarminClient = _garmin_client()

    # Assert that the result is an instance of GarminClient
    assert isinstance(result, GarminClient)


@mock.patch('garminworkouts.__main__.account')
def test__garmin_client_missing_email(mock_account) -> None:
    # Mock the account module without EMAIL
    del mock_account.EMAIL
    mock_account.PASSWORD = 'password123'

    # Call the _garmin_client function and assert it raises AttributeError
    with pytest.raises(AttributeError, match="account module must define EMAIL and PASSWORD"):
        _garmin_client()


@mock.patch('garminworkouts.__main__.account')
def test__garmin_client_missing_password(mock_account) -> None:
    # Mock the account module without PASSWORD
    mock_account.EMAIL = 'test@example.com'
    del mock_account.PASSWORD

    # Call the _garmin_client function and assert it raises AttributeError
    with pytest.raises(AttributeError, match="account module must define EMAIL and PASSWORD"):
        _garmin_client()


@mock.patch('garminworkouts.__main__._garmin_client')
def test_trainingplan_reset(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

    with mock.patch.object(authed_gclient, 'trainingplan_reset') as mock_trainingplan_reset:
        mock_trainingplan_reset.return_value = None

        command_trainingplan_reset(args)
        assert mock_trainingplan_reset.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_trainingplan_import(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

    with mock.patch.object(authed_gclient, 'update_workouts') as mock_update_workouts, \
         mock.patch.object(authed_gclient, 'get_calendar') as mock_get_calendar, \
         mock.patch.object(authed_gclient, 'update_notes') as mock_update_notes:
        mock_update_workouts.return_value = None
        mock_get_calendar.return_value = None, None, None
        mock_update_notes.return_value = None

        command_trainingplan_import(args)
        assert mock_update_workouts.call_count == 1
        assert mock_get_calendar.call_count == 1
        assert mock_update_notes.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_event_import(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(trainingplan='Races/*.yaml')

    with mock.patch.object(authed_gclient, 'update_workouts') as mock_update_workouts, \
            mock.patch.object(authed_gclient, 'get_calendar') as mock_get_calendar, \
            mock.patch.object(authed_gclient, 'update_events') as mock_update_events:
        mock_update_workouts.return_value = None
        mock_get_calendar.return_value = None, None, None
        mock_update_events.return_value = None

        command_event_import(args)
        assert mock_update_workouts.call_count == 1
        assert mock_get_calendar.call_count == 1
        assert mock_update_events.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_trainingplan_metrics(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

    with mock.patch.object(Workout, 'load_metrics') as mock_trainingplan_metrics:
        mock_trainingplan_metrics.return_value = None

        command_trainingplan_metrics(args)
        assert mock_trainingplan_metrics.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_workout_export(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

    with mock.patch.object(authed_gclient, 'workout_export') as mock_workout_export:
        mock_workout_export.return_value = None

        command_workout_export(args)
        assert mock_workout_export.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_workout_export_yaml(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

    with mock.patch.object(authed_gclient, 'external_workout_export_yaml') as mock_workout_export:
        mock_workout_export.return_value = None

        command_workout_export_yaml(args)
        assert mock_workout_export.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_workout_schedule(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(id='1', date='2021-01-01')

    with mock.patch.object(authed_gclient, 'schedule_workout') as mock_schedule_workout:
        mock_schedule_workout.return_value = None

        command_workout_schedule(args)
        assert mock_schedule_workout.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_workout_get(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(id='1')

    with mock.patch.object(Workout, 'print_workout_json') as mock_workout_print, \
         mock.patch.object(authed_gclient, 'get_workout') as mock_workout_get:
        mock_workout_print.return_value = None
        mock_workout_get.return_value = None

        command_workout_get(args)
        assert mock_workout_get.call_count == 1
        assert mock_workout_print.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_event_get(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(id='1')

    with mock.patch.object(Event, 'print_event_json') as mock_event_print, \
            mock.patch.object(authed_gclient, 'get_event') as mock_event_get:
        mock_event_print.return_value = None
        mock_event_get.return_value = None

        command_event_get(args)
        assert mock_event_get.call_count == 1
        assert mock_event_print.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_workout_delete(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(workout_id='1')

    with mock.patch.object(authed_gclient, 'delete_workout') as mock_delete_workout:
        mock_delete_workout.return_value = None

        command_workout_delete(args)
        assert mock_delete_workout.call_count == 1
