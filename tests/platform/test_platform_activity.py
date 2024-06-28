from garminworkouts.garmin.garminclient import GarminClient


def test_get_activities_by_date(authed_gclient: GarminClient) -> None:
    act_list = authed_gclient.get_activities_by_date()
    assert act_list
