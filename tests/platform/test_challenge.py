import pytest
from unittest.mock import patch
from datetime import datetime
from garminworkouts.garmin.garminclient import GarminClient
import account


@pytest.fixture
def garmin_client() -> GarminClient:
    return GarminClient(account.EMAIL, account.PASSWORD)


def test_list_challenge_positive(garmin_client: GarminClient) -> None:
    with patch.object(garmin_client, 'get') as mock_get, \
            patch.object(garmin_client, 'post') as mock_post:

        mock_get.return_value.json.return_value = [{'uuid': '123'}]

        garmin_client.list_challenge()

        mock_get.assert_called_once_with(f"{GarminClient._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/available")
        mock_post.assert_called_once_with(
            f"{GarminClient._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge"
            f"/123/optIn/{datetime.today().strftime('%Y-%m-%d')}")


def test_list_challenge_negative(garmin_client: GarminClient) -> None:
    with patch.object(garmin_client, 'get') as mock_get, \
            patch.object(garmin_client, 'post') as mock_post:

        mock_get.return_value.json.return_value = []

        garmin_client.list_challenge()

        mock_get.assert_called_once_with(f"{GarminClient._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/available")
        mock_post.assert_not_called()
