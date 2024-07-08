from unittest.mock import patch
from garminworkouts.garmin.garminclient import GarminClient


def test_user_zones_save_hr_zones_called(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'save_hr_zones') as mock_save_hr_zones, \
            patch.object(authed_gclient, 'save_power_zones') as mock_save_power_zones:
        authed_gclient.user_zones()
        mock_save_hr_zones.assert_called_once()
        mock_save_power_zones.assert_called_once()
