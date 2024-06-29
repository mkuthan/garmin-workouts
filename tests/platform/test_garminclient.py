from unittest.mock import patch, MagicMock
from garminworkouts.garmin.garminclient import GarminClient


def test_enter(authed_gclient: GarminClient) -> None:
    assert authed_gclient.__enter__()


def test_exit(authed_gclient: GarminClient) -> None:
    assert authed_gclient.__exit__(None, None, None) is None


def test_get_mfa(authed_gclient: GarminClient) -> None:
    with patch('builtins.input', return_value='mocked input value'):
        ans: str = authed_gclient.get_mfa()
        assert ans == 'mocked input value'


def custom_get_side_effect_no_error(arg) -> MagicMock:
    # Custom logic to return different values based on args or kwargs
    if arg == "/userprofile-service/userprofile/user-settings":
        return MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        return MagicMock(json=lambda: [{"version": GarminClient._GARMIN_VERSION}])
    else:
        return MagicMock(status_code=404)


def custom_get_side_effect_update_version(arg) -> MagicMock:
    # Custom logic to return different values based on args or kwargs
    if arg == "/userprofile-service/userprofile/user-settings":
        return MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        return MagicMock(json=lambda: [{"version": "1.0.0"}])
    else:
        return MagicMock(status_code=404)


def custom_get_side_effect_error_version(arg) -> MagicMock:
    # Custom logic to return different values based on args or kwargs
    if arg == "/userprofile-service/userprofile/user-settings":
        return MagicMock(json=lambda: {"userData": {"measurementSystem": "metric"}})
    elif arg == "/info-service/api/system/release-system":
        return MagicMock(json=lambda: [{"version2": "1.0.0"}])
    else:
        return MagicMock(status_code=404)


def test_login_no_error(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        mock_get.side_effect = custom_get_side_effect_no_error
        assert authed_gclient.login(tokenstore=None)


def test_login_update_version(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        mock_get.side_effect = custom_get_side_effect_update_version
        assert authed_gclient.login(tokenstore=None)


def test_login_error_version(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        mock_get.side_effect = custom_get_side_effect_error_version
        assert authed_gclient.login(tokenstore=None)
