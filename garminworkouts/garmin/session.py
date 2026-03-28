from pathlib import Path

try:
    from garminconnect import (
        Garmin,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
    )
except ModuleNotFoundError:  # pragma: no cover
    Garmin = None

    class GarminConnectAuthenticationError(Exception):
        pass

    class GarminConnectConnectionError(Exception):
        pass


class SessionLoginRequiredError(RuntimeError):
    pass


LOGIN_REQUIRED_MESSAGE = "You're not logged in. Run 'garmin-workouts login' first."


def _require_garmin():
    if Garmin is None:
        raise RuntimeError("garminconnect dependency is required")
    return Garmin


def _normalize_tokenstore(session_file: str) -> str:
    session_path = Path(session_file)
    if session_path.exists() and session_path.is_file():
        return f"{session_file}.session"
    return session_file


def login(username: str, password: str, session_file: str) -> None:
    garmin_cls = _require_garmin()
    api = garmin_cls(username, password)
    api.login(tokenstore=_normalize_tokenstore(session_file))


def connect(session_file: str) -> Garmin:
    garmin_cls = _require_garmin()
    try:
        api = garmin_cls()
        api.login(tokenstore=_normalize_tokenstore(session_file))
        return api
    except (
        FileNotFoundError,
        OSError,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
    ) as exc:
        raise SessionLoginRequiredError(LOGIN_REQUIRED_MESSAGE) from exc


def disconnect(_api) -> None:
    return None
