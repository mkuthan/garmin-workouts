from typing import Any
from garminworkouts.garmin.garminclient import GarminClient


def test_get_power_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/sports/all"
    assert authed_gclient.get(url)


def test_save_power_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/all"
    zones: list[dict[str, Any]] = [
        {
            "sport": "CYCLING",
            "functionalThresholdPower": str(275),
            "zone1Floor": str(179),
            "zone2Floor": str(220),
            "zone3Floor": str(248),
            "zone4Floor": str(275),
            "zone5Floor": str(316),
            "zone6Floor": str(358),
            "zone7Floor": str(412),
            "userLocalTime": None
        },
        {
            "sport": "RUNNING",
            "functionalThresholdPower": str(380),
            "zone1Floor": str(247),
            "zone2Floor": str(304),
            "zone3Floor": str(342),
            "zone4Floor": str(380),
            "zone5Floor": str(437),
            "zone6Floor": str(0.0),
            "zone7Floor": str(0.0),
            "userLocalTime": None
        }
    ]
    assert authed_gclient.put(url, json=zones)
