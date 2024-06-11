from datetime import date
from garminworkouts.garmin.garminclient import GarminClient


def test_get_RHR(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._WELLNESS_SERVICE_ENDPOINT}/wellness/dailyHeartRate"
    params: dict = {
        "date": date.today(),
    }
    assert authed_gclient.get(url, params=params)


def test_get_hr_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
    assert authed_gclient.get(url)


def test_save_hr_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
    zones: dict = authed_gclient.get(url).json()
    assert authed_gclient.put(url, json=zones)
