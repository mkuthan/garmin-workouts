import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from garminworkouts.garmin.garminwellness import GarminWellness


@pytest.fixture
def garmin_wellness():
    return GarminWellness(email='test@example.com', password='password123')


@patch('garminworkouts.garmin.garminwellness.GarminWellness.get')
def test_get_RHR(mock_get, garmin_wellness):
    mock_response = MagicMock()
    mock_response.json.return_value = {'restingHeartRate': '60'}
    mock_get.return_value = mock_response

    result = garmin_wellness.get_RHR()
    assert result == 60
    mock_get.assert_called_once_with('/wellness-service/wellness/dailyHeartRate', params={'date': date.today()})
