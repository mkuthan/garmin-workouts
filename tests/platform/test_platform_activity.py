import pytest
from datetime import date, timedelta
from requests import Response
from garminworkouts.garmin.garminclient import GarminClient


@pytest.mark.vcr
def test_get_activities_by_date(authed_gclient: GarminClient) -> None:
    startdate: date = date.today() + timedelta(weeks=-4)
    enddate: str = date.today().isoformat()
    activitytype = None

    activities: list = []
    start = 0
    limit = 20

    url: str = f"{GarminClient._ACTIVITY_LIST_SERVICE_ENDPOINT}/activities/search/activities"
    params: dict[str, str] = {
        "startDate": str(startdate),
        "endDate": str(enddate),
        "start": str(start),
        "limit": str(limit),
    }
    if activitytype:
        params["activityType"] = str(activitytype)

    print(f"Requesting activities by date from {startdate} to {enddate}")
    while True:
        params["start"] = str(start)
        print(f"Requesting activities {start} to {start+limit}")
        act: Response = authed_gclient.get(url, params=params)
        assert act
        if act.json() != []:
            activities.extend(act)
            start = start + limit
        else:
            break
