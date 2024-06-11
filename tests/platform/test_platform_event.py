import pytest
from datetime import date
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.event import Event


@pytest.mark.vcr
def test_list_events(authed_gclient: GarminClient) -> None:
    assert authed_gclient.list_events()


@pytest.mark.vcr
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
    event_id = Event.extract_event_id(e)
    assert authed_gclient.get_event(event_id)
    assert authed_gclient.update_event(event_id, e)
    assert authed_gclient.delete_event(event_id)
