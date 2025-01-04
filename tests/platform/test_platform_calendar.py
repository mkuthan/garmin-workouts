from datetime import date
from unittest.mock import MagicMock, patch
from garminworkouts.garmin.garminclient import GarminClient


def test_get_calendar(authed_gclient: GarminClient) -> None:
    year = str(date.today().year)
    month = str(date.today().month - 1)
    url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}"

    assert authed_gclient.get(url)

    updateable_elements, checkable_elements, note_elements = authed_gclient.get_calendar(date.today())
    assert len(updateable_elements) >= 0
    assert len(checkable_elements) >= 0
    assert len(note_elements) >= 0


def test_get_calendar_workout(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get, \
            patch.object(authed_gclient, 'delete') as mock_delete:
        mock_get.return_value.json.return_value = {
            "calendarItems": [
                {
                    "itemType": "workout",
                    "workoutId": "123",
                    "date": "2021-01-01",
                    "title": "Test Workout",
                },
            ],
        }
        mock_delete.return_value = MagicMock(status_code=200)

        updateable_elements, checkable_elements, note_elements = authed_gclient.get_calendar(date.today())
        assert len(updateable_elements) >= 0
        assert len(checkable_elements) >= 0
        assert len(note_elements) >= 0


def custom_get_side_effect_activity(arg) -> MagicMock:
    date_w: date = date.today()
    year = str(date_w.year)
    month = str(date_w.month - 1)
    activity_id = '123'

    a = MagicMock(status_code=404)
    if arg == f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}":
        a = MagicMock(json=lambda: {
            "calendarItems": [
                {
                    "itemType": "activity",
                    "id": "123",
                    "date": "2021-01-01",
                    "title": "Test Activity",
                },
            ],
        })
    elif arg == f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/{activity_id}/workouts":
        a = MagicMock(status_code=200, json=lambda: [{
            "workoutName": "Test Workout",
        }])
    return a


def test_get_calendar_activity(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        mock_get.side_effect = custom_get_side_effect_activity

        updateable_elements, checkable_elements, note_elements = authed_gclient.get_calendar(date.today())
        assert len(updateable_elements) >= 0
        assert len(checkable_elements) >= 0
        assert len(note_elements) >= 0


def custom_get_side_effect_note(arg) -> MagicMock:
    date_w: date = date.today()
    year = str(date_w.year)
    month = str(date_w.month - 1)

    a = MagicMock(status_code=404)
    if arg == f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}":
        a = MagicMock(json=lambda: {
            "calendarItems": [
                {
                    "itemType": "note",
                    "id": "123",
                    "date": "2021-01-01",
                    "trainingPlanId": "123",
                },
                {
                    "itemType": "note",
                    "id": "123",
                    "date": "2021-01-01",
                    "trainingPlanId": None,
                },
            ],
        })
    return a


def custom_delete_side_effect_note(arg) -> MagicMock:
    plan_id = '123'
    note_id = '123'

    a = MagicMock(status_code=404)
    if arg == f"{GarminClient._TRAINING_PLAN_SERVICE_ENDPOINT}/noteTask/{plan_id}/{note_id}":
        a = MagicMock(status_code=200, json=lambda: {
            "noteName": "Test Note",
        })
    elif arg == f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/note/{note_id}":
        a = MagicMock(status_code=200, json=lambda: {
            "noteName": "Test Note",
        })
    return a


def test_get_calendar_note(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get, \
         patch.object(authed_gclient, 'delete') as mock_delete:
        mock_get.side_effect = custom_get_side_effect_note
        mock_delete.side_effect = custom_delete_side_effect_note

        updateable_elements, checkable_elements, note_elements = authed_gclient.get_calendar(date.today())
        assert len(updateable_elements) >= 0
        assert len(checkable_elements) >= 0
        assert len(note_elements) >= 0
