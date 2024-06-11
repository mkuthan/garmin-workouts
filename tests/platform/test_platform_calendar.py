from datetime import date
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
