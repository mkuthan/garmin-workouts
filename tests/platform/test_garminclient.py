import os
from unittest.mock import Mock, patch, MagicMock
from garminworkouts.garmin.garminclient import GarminClient


def test_enter(authed_gclient: GarminClient) -> None:
    assert authed_gclient.__enter__()


def test_exit(authed_gclient: GarminClient) -> None:
    assert authed_gclient.__exit__(None, None, None) is None


def test_get_mfa(authed_gclient: GarminClient) -> None:
    with patch('builtins.input', return_value='mocked input value'):
        ans: str = authed_gclient.get_mfa()
        assert ans == 'mocked input value'


def custom_get_side_effect_no_error(arg) -> MagicMock:
    # Custom logic to return different values based on args or kwargs
    if arg == "/userprofile-service/userprofile/user-settings":
        return MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        return MagicMock(json=lambda: [{"version": GarminClient._GARMIN_VERSION}])
    else:
        return MagicMock(status_code=404)


def custom_get_side_effect_update_version(arg) -> MagicMock:
    # Custom logic to return different values based on args or kwargs
    if arg == "/userprofile-service/userprofile/user-settings":
        return MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        return MagicMock(json=lambda: [{"version": "1.0.0"}])
    else:
        return MagicMock(status_code=404)


def custom_get_side_effect_error_version(arg) -> MagicMock:
    # Custom logic to return different values based on args or kwargs
    if arg == "/userprofile-service/userprofile/user-settings":
        return MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        return MagicMock(json=lambda: [{"version2": "1.0.0"}])
    else:
        return MagicMock(status_code=404)


def custom_get_side_effect_error_version2(arg) -> MagicMock:
    # Custom logic to return different values based on args or kwargs
    if arg == "/userprofile-service/userprofile/user-settings":
        return MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        return MagicMock(json=lambda: [])
    else:
        return MagicMock(status_code=404)


def test_login_no_error(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        mock_get.side_effect = custom_get_side_effect_no_error
        assert authed_gclient.login(tokenstore=None)


def test_login_update_version(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        mock_get.side_effect = custom_get_side_effect_update_version
        assert authed_gclient.login(tokenstore=None)


def test_login_error_version(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        mock_get.side_effect = custom_get_side_effect_error_version
        assert authed_gclient.login(tokenstore=None)


def test_login_error_version2(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        mock_get.side_effect = custom_get_side_effect_error_version2
        assert authed_gclient.login(tokenstore=None)


def test_activity_list(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get_activities_by_date') as mock_get_activities_by_date:
        mock_get_activities_by_date.return_value = [
            {"activityId": "1", "activityType": "running"},
            {"activityId": "2", "activityType": "running"},
            {"activityId": "3", "activityType": "cycling"},
        ]
        with patch.object(authed_gclient, 'download_activity') as mock_download_activity:
            authed_gclient.activity_list()
            assert mock_get_activities_by_date.call_count == 1
            assert mock_download_activity.call_count == 3


def test_updateGarmin(authed_gclient: GarminClient) -> None:
    authed_gclient.version = "2.0.0"

    with patch.object(authed_gclient, 'get_types') as mock_get_types:
        authed_gclient.updateGarmin()
        assert mock_get_types.call_count == 1

    authed_gclient.version = GarminClient._GARMIN_VERSION
    authed_gclient.updateGarmin()


def test_workout_list(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'list_workouts') as mock_list_workouts:
        mock_list_workouts.return_value = [
            {"workoutId": "1", "workoutName": "Workout 1"},
            {"workoutId": "2", "workoutName": "Workout 2"},
            {"workoutId": "3", "workoutName": "Workout 3"},
        ]
        authed_gclient.workout_list()
        assert mock_list_workouts.call_count == 1


def test_event_list(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'list_events') as mock_list_events:
        mock_list_events.return_value = [
            {"eventId": "1", "eventName": "Event 1", "date": "2021-01-01", "location": "Location 1"},
            {"eventId": "2", "eventName": "Event 2", "date": "2021-01-02", "location": "Location 2"},
            {"eventId": "3", "eventName": "Event 3", "date": "2021-01-03", "location": "Location 3"},
        ]
        authed_gclient.event_list()
        assert mock_list_events.call_count == 1


def test_trainingplan_list(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'list_trainingplans') as mock_list_trainingplans:
        mock_list_trainingplans.return_value = [
            {
                "trainingPlanId": "1",
                "trainingType": {"typeKey": "running"},
                "trainingSubType": {"subTypeKey": "5k"},
                "trainingLevel": {"levelKey": "beginner"},
                "trainingVersion": {"versionName": "1.0"},
                "name": "Training Plan 1",
                "description": "Description 1",
                "durationInWeeks": 12,
                "avgWeeklyWorkouts": 3,
            }
        ]
        authed_gclient.trainingplan_list()
        assert mock_list_trainingplans.call_count == 1


def test_workout_export(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'list_workouts') as mock_list_workouts:
        mock_list_workouts.return_value = [
            {"workoutId": "1", "workoutName": "Workout 1"},
            {"workoutId": "2", "workoutName": "Workout 2"},
            {"workoutId": "3", "workoutName": "Workout 3"},
        ]
        with patch.object(authed_gclient, 'download_workout') as mock_download_workout:
            authed_gclient.workout_export(Mock(directory='path/to/export'))
            assert mock_list_workouts.call_count == 1
            assert mock_download_workout.call_count == 3


def test_find_events(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'find_events') as mock_find_events:
        mock_find_events.return_value = [
            [
                b'{"eventType": "running", "eventRef": "123", "detailsEndpoints": [{"url": "/event/123"}]}',
                b'{"eventType": "cycling", "eventRef": "456", "detailsEndpoints": [{"url": "/event/456"}]}'
            ],
            [
                b'{"eventType": "swimming", "eventRef": "789", "detailsEndpoints": [{"url": "/event/789"}]}'
            ]
        ]
        with patch.object(authed_gclient, 'get') as mock_get:
            mock_get.side_effect = [
                MagicMock(json=lambda: {"eventRef": "1", "detailsEndpoints": [{"url": "/event/1"}]}),
                MagicMock(json=lambda: {"eventRef": "2", "detailsEndpoints": [{"url": "/event/2"}]}),
                MagicMock(json=lambda: {"eventRef": "3", "detailsEndpoints": [{"url": "/event/3"}]}),
                MagicMock(json=lambda: {"eventRef": "4", "detailsEndpoints": [{"url": "/event/4"}]})
            ]

            authed_gclient._find_events()
            assert mock_find_events.call_count == 1
            assert mock_get.call_count == 3
    os.remove("exported/events/running/123.yaml")
    os.remove("exported/events/cycling/456.yaml")
    os.remove("exported/events/swimming/789.yaml")
