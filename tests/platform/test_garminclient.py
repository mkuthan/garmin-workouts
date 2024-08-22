import argparse
import os
from unittest.mock import Mock, patch, MagicMock
from garminworkouts.garmin.garminclient import GarminClient
from datetime import date, timedelta
from garminworkouts.models.note import Note
from garminworkouts.models.settings import settings


def test_enter(authed_gclient: GarminClient) -> None:
    assert authed_gclient.__enter__()


def test_exit(authed_gclient: GarminClient) -> None:
    assert authed_gclient.__exit__(None, None, None) is None


def test_get_mfa(authed_gclient: GarminClient) -> None:
    with patch('builtins.input', return_value='mocked input value'):
        ans: str = authed_gclient.get_mfa()
        assert ans == 'mocked input value'


def custom_get_side_effect_no_error(arg) -> MagicMock:
    a = MagicMock(status_code=404)
    if arg == "/userprofile-service/userprofile/user-settings":
        a = MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        a = MagicMock(json=lambda: [{"version": GarminClient._GARMIN_VERSION}])
    return a


def custom_get_side_effect_update_version(arg) -> MagicMock:
    a = MagicMock(status_code=404)
    if arg == "/userprofile-service/userprofile/user-settings":
        a = MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        a = MagicMock(json=lambda: [{"version": "1.0.0"}])
    return a


def custom_get_side_effect_error_version(arg) -> MagicMock:
    a = MagicMock(status_code=404)
    if arg == "/userprofile-service/userprofile/user-settings":
        a = MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        a = MagicMock(json=lambda: [{"version2": "1.0.0"}])
    return a


def custom_get_side_effect_error_version2(arg) -> MagicMock:
    a = MagicMock(status_code=404)
    if arg == "/userprofile-service/userprofile/user-settings":
        a = MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        a = MagicMock(json=lambda: [])
    return a


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


def test_workout_update_delete_workout(authed_gclient: GarminClient) -> None:
    date_today: date = date.today()
    date_plus_days: date = date_today + timedelta(days=7)
    item: dict = {
        "title": "Workout 1",
        "itemType": "workout",
        "date": (date_today - timedelta(days=1)).isoformat(),
        "workoutId": "1",
        "trainingPlanId": None
    }
    updateable_elements: list = []
    with patch.object(authed_gclient, 'delete_workout') as mock_delete_workout:
        authed_gclient.workout_update(date_today, updateable_elements, date_plus_days, item,
                                      date_today - timedelta(days=1))
        mock_delete_workout.assert_called_once()


def test_workout_update_add_workout(authed_gclient: GarminClient) -> None:
    date_today: date = date.today()
    date_plus_days: date = date_today + timedelta(days=7)
    item: dict = {
        "title": "Workout 2",
        "itemType": "workout",
        "date": (date_today + timedelta(days=1)).isoformat(),
        "workoutId": "2",
        "trainingPlanId": None
    }
    updateable_elements: list = []
    authed_gclient.workout_update(date_today, updateable_elements, date_plus_days, item,
                                  date_today + timedelta(days=1))
    assert "Workout 2" == updateable_elements[0]


def test_workout_update_delete_trainingplan(authed_gclient: GarminClient) -> None:
    date_today: date = date.today()
    date_plus_days: date = date_today + timedelta(days=7)
    item: dict[str, str] = {
        "title": "Workout 1",
        "itemType": "workout",
        "date": (date_today - timedelta(days=1)).isoformat(),
        "workoutId": "1",
        "trainingPlanId": "1"
    }
    updateable_elements: list = []
    with patch.object(authed_gclient, 'delete_training_plan_workout') as mock_delete_workout:
        authed_gclient.workout_update(date_today, updateable_elements, date_plus_days, item,
                                      date_today - timedelta(days=1))
        mock_delete_workout.assert_called_once()


def test_note_update_delete_note(authed_gclient: GarminClient) -> None:
    date_today: date = date.today()
    date_plus_days: date = date_today + timedelta(days=7)
    item: dict = {
        "noteName": "Note 1",
        "itemType": "note",
        "date": (date_today - timedelta(days=1)).isoformat(),
        "id": "1",
        "trainingPlanId": None
    }
    updateable_elements: list = []
    with patch.object(authed_gclient, 'delete_note') as mock_delete_note:
        authed_gclient.note_update(date_today, updateable_elements, date_plus_days, item,
                                   date_today - timedelta(days=1))
        mock_delete_note.assert_called_once()


def test_note_update_add_note(authed_gclient: GarminClient) -> None:
    date_today: date = date.today()
    date_plus_days: date = date_today + timedelta(days=7)
    item: dict = {
        "noteName": "Note 2",
        "itemType": "note",
        "date": (date_today + timedelta(days=1)).isoformat(),
        "id": "2",
        "trainingPlanId": None
    }
    updateable_elements: dict = {}
    with patch.object(authed_gclient, 'get_note') as mock_get_note:
        mock_get_note.return_value.json.return_value = {
            "noteName": "Note 2",
            "content": "Content 2",
            "date": (date_today + timedelta(days=1)).isoformat()
        }
        authed_gclient.note_update(date_today, updateable_elements, date_plus_days, item,
                                   date_today + timedelta(days=1))
    assert "Note 2" in updateable_elements


def test_note_update_add_note_tp(authed_gclient: GarminClient) -> None:
    date_today: date = date.today()
    date_plus_days: date = date_today + timedelta(days=7)
    item: dict = {
        "noteName": "Note 2",
        "itemType": "note",
        "date": (date_today + timedelta(days=1)).isoformat(),
        "id": "2",
        "trainingPlanId": "1"
    }
    updateable_elements: dict = {}
    with patch.object(authed_gclient, 'get_note') as mock_get_note:
        mock_get_note.return_value.json.return_value = {
            "noteName": "Note 2",
            "content": "Content 2",
            "date": (date_today + timedelta(days=1)).isoformat()
        }
        authed_gclient.note_update(date_today, updateable_elements, date_plus_days, item,
                                   date_today + timedelta(days=1))
    assert "Note 2" in updateable_elements


def test_note_update_delete_trainingplan(authed_gclient: GarminClient) -> None:
    date_today: date = date.today()
    date_plus_days: date = date_today + timedelta(days=7)
    item: dict[str, str] = {
        "title": "Note 1",
        "itemType": "note",
        "date": (date_today - timedelta(days=1)).isoformat(),
        "workoutId": "1",
        "trainingPlanId": "1"
    }
    updateable_elements: list = []
    with patch.object(authed_gclient, 'delete_training_plan_workout') as mock_delete_workout:
        authed_gclient.workout_update(date_today, updateable_elements, date_plus_days, item,
                                      date_today - timedelta(days=1))
        mock_delete_workout.assert_called_once()


def test_update_workouts(authed_gclient: GarminClient) -> None:
    ue: list[str] = ["Workout 1", "Workout 2"]
    args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')
    workouts, notes, plan = settings(args)

    with patch.object(authed_gclient, 'list_workouts') as mock_list_workouts, \
            patch.object(authed_gclient, 'update_workout') as mock_update_workout, \
            patch.object(authed_gclient, 'save_workout') as mock_save_workout, \
            patch.object(authed_gclient, 'schedule_workout') as mock_schedule_workout:
        mock_list_workouts.return_value = [
            {"workoutId": "1", "workoutName": "Workout 1"},
            {"workoutId": "2", "workoutName": "Workout 2"},
        ]
        authed_gclient.update_workouts(ue, workouts, plan)

        assert mock_list_workouts.call_count == 1
        assert mock_update_workout.call_count == 0
        assert mock_save_workout.call_count == 5
        assert mock_schedule_workout.call_count == 5


def test_update_notes(authed_gclient: GarminClient) -> None:
    ue: dict = {}
    args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')
    workouts, notes, plan = settings(args)

    with patch.object(authed_gclient, 'update_note') as mock_update_note, \
            patch.object(Note, 'create_note') as mock_create_note, \
            patch.object(authed_gclient, 'save_note') as mock_save_note:
        mock_create_note.return_value = {
            "noteId": "1",
            "noteName": "Rest",
            "content": "Rest",
            "date": "2021-01-01"
        }
        authed_gclient.update_notes(ue, notes, plan)

        assert mock_update_note.call_count == 0
        assert mock_save_note.call_count == 8


def test_update_events_no_events(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'list_events') as mock_list_events, \
            patch.object(authed_gclient, 'list_workouts') as mock_list_workouts, \
            patch.object(authed_gclient, 'save_event') as mock_save_event:
        mock_list_events.return_value = []
        mock_list_workouts.return_value = []

        authed_gclient.update_events([])

        assert mock_list_events.call_count == 1
        assert mock_list_workouts.call_count == 1
        assert mock_save_event.call_count == 0
