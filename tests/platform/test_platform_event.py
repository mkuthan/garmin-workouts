from datetime import date
import shutil
from unittest.mock import patch
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.event import Event


def test_list_events(authed_gclient: GarminClient) -> None:
    # Call the method under test
    events = list(authed_gclient.list_events())

    # Assert that the returned value is a list
    assert isinstance(events, list)

    # Assert that the list is not empty
    assert len(events) > 0


def test_find_events(authed_gclient: GarminClient) -> None:
    # Call the method under test
    events = list(authed_gclient.find_events())

    # Assert that the returned value is a list
    assert isinstance(events, list)

    # Assert that the list is not empty
    assert len(events) > 0
    shutil.rmtree('./exported')


def mock_generator():
    # Mock data: list of dictionaries to be yielded
    mock_data = [
        [{
            'eventRef': '123',
            'eventName': 'ABC',
            'eventDate': '2024-07-07',
            'eventStartTime': {'startTimeHhMm': '06:15', 'timeZoneId': 'Pacific/Port_Moresby'},
            'eventUrl': 'https://www.123.com', 'registrationUrl': None,
            'completionTargets': [{'value': 42195.0, 'unit': 'meter'}],
            'locationStartPoint': {'lat': -27.9713, 'lon': 153.3986},
            'eventType': 'running',
            'administrativeArea': {
                'countryCode': 'AU'},
            'detailsEndpoints': [
                {
                    'view': 'GC',
                    'url': '/calendar-service/event/d7f724cd-227a-44c0-8d4f-74af3768144c/shareable'
                }],
            }],
        [{
            'eventRef': '456',
            'eventName': 'ABC',
            'eventDate': '2024-07-07',
            'eventStartTime': {'startTimeHhMm': '06:15', 'timeZoneId': 'Pacific/Port_Moresby'},
            'eventUrl': 'https://www.123.com', 'registrationUrl': None,
            'completionTargets': [{'value': 42195.0, 'unit': 'meter'}],
            'locationStartPoint': {'lat': -27.9713, 'lon': 153.3986},
            'eventType': 'running',
            'administrativeArea': None,
            'detailsEndpoints': [
                {
                    'view': 'GC',
                    'url': '/calendar-service/event/d7f724cd-227a-44c0-8d4f-74af3768144c/shareable'
                }],
        }]
    ]

    # Yield each dictionary in the mock data
    for item in mock_data:
        yield item


def test_find_events2(authed_gclient: GarminClient) -> None:
    # Call the method under test
    with patch.object(authed_gclient, 'find_events') as mock_find_events:
        mock_find_events.side_effect = mock_generator
        assert authed_gclient._find_events() is None
        shutil.rmtree('./exported')


def test_events_methods(authed_gclient: GarminClient) -> None:
    event_config: dict = {
        'name': 'Name',
        'date': {
            'day': int(1),
            'month': int(date.today().month),
            'year': int(date.today().year + 1),
        },
        'url': 'https://www.123.com/',
        'location': 'London, UK',
        'time': '19:00',
        'distance': 5,
        'goal': '20:00',
        'sport': 'running'}

    event = Event(event_config)
    e: dict = event.create_event()
    assert e
    e = authed_gclient.save_event(e)
    assert e
    event_id: str = Event.extract_event_id(e)
    assert authed_gclient.get_event(event_id)
    assert authed_gclient.update_event(event_id, e)
    assert authed_gclient.delete_event(event_id)
