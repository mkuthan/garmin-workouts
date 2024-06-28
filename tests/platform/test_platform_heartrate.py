from unittest.mock import patch
from requests import Response
from garminworkouts.garmin.garminclient import GarminClient


def test_get_RHR(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        mock_get.return_value.json.return_value = {'restingHeartRate': 45}

        rhr: int = authed_gclient.get_RHR()
        assert rhr == 45


def test_get_and_save_hr_zones(authed_gclient: GarminClient) -> None:
    zones: dict = authed_gclient.get_hr_zones()
    assert zones
    up_zones: Response = authed_gclient.save_hr_zones(zones)
    assert up_zones
