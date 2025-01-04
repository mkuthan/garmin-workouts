import pytest
from unittest.mock import patch, MagicMock
from garminworkouts.garmin.garminevent import GarminEvent


@pytest.fixture
def garmin_event():
    return GarminEvent(email='test@example.com', password='password123')


@patch.object(GarminEvent, 'get')
def test_list_events(mock_get, garmin_event):
    mock_response = MagicMock()
    mock_response.json.side_effect = [
        [{'id': 1, 'name': 'Event 1'}, {'id': 2, 'name': 'Event 2'}],
        []
    ]
    mock_get.return_value = mock_response

    events = list(garmin_event.list_events(batch_size=2))

    assert len(events) == 2
    assert events[0]['id'] == 1
    assert events[1]['id'] == 2
