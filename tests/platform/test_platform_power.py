from garminworkouts.garmin.garminclient import GarminClient
from requests import Response


def test_get_and_save_hr_zones(authed_gclient: GarminClient) -> None:
    zones: dict = authed_gclient.get_power_zones()
    assert zones
    up_zones: Response = authed_gclient.save_power_zones(zones)
    assert up_zones
