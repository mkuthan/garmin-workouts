from unittest.mock import patch
from garminworkouts.garmin.garminclient import GarminClient


def test_user_zones_save_hr_zones_called(authed_client: GarminClient) -> None:
    with patch('authed_client.save_hr_zones') as mock_save_hr_zones, \
         patch('garminworkouts.garmin.garminbiometric.GarminBiometric.save_power_zones') as mock_save_power_zones:
        authed_client.user_zones()
        mock_save_hr_zones.assert_called_once()
        mock_save_power_zones.assert_called_once()
