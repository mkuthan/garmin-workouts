import pytest
from unittest.mock import patch
from datetime import datetime
from garminworkouts.garmin.garminclient import GarminClient


@pytest.mark.vcr
def test_list_challenge_positive(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get, \
            patch.object(authed_gclient, 'post') as mock_post:

        mock_get.return_value.json.return_value = [{'uuid': '123'}]

        authed_gclient.list_challenge()

        mock_get.assert_called_once_with(f"{GarminClient._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/available")
        mock_post.assert_called_once_with(
            f"{GarminClient._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge"
            f"/123/optIn/{datetime.today().strftime('%Y-%m-%d')}")


@pytest.mark.vcr
def test_list_challenge_negative(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get, \
            patch.object(authed_gclient, 'post') as mock_post:

        mock_get.return_value.json.return_value = []

        authed_gclient.list_challenge()

        mock_get.assert_called_once_with(f"{GarminClient._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/available")
        mock_post.assert_not_called()
