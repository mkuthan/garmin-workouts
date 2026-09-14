import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from garminworkouts.garmin.session import SessionLoginRequiredError, connect, login


class SessionTestCase(unittest.TestCase):
    @patch("garminworkouts.garmin.session.Garmin")
    def test_login_calls_garmin_login_with_tokenstore(self, garmin_cls):
        client = garmin_cls.return_value

        login(username="user", password="pass", session_file="/tmp/garmin-session")

        garmin_cls.assert_called_once_with("user", "pass")
        client.login.assert_called_once_with(tokenstore="/tmp/garmin-session")

    @patch("garminworkouts.garmin.session.Garmin")
    def test_connect_loads_existing_session_file(self, garmin_cls):
        client = garmin_cls.return_value

        result = connect(session_file="/tmp/garmin-session")

        garmin_cls.assert_called_once_with()
        self.assertIs(result, client)
        client.login.assert_called_once_with(tokenstore="/tmp/garmin-session")

    @patch("garminworkouts.garmin.session.Garmin")
    def test_connect_raises_login_required_when_session_missing(self, garmin_cls):
        client = garmin_cls.return_value
        client.login.side_effect = FileNotFoundError("session not found")

        with self.assertRaises(SessionLoginRequiredError):
            connect(session_file="/tmp/missing")

    @patch("garminworkouts.garmin.session.Garmin")
    def test_login_uses_file_path_fallback_directory_for_tokenstore(self, garmin_cls):
        client = garmin_cls.return_value

        with TemporaryDirectory() as tmp:
            session_file = Path(tmp) / "legacy-cookies.txt"
            session_file.write_text("cookies")

            login(username="user", password="pass", session_file=str(session_file))

            client.login.assert_called_once_with(tokenstore=f"{session_file}.session")

    @patch("garminworkouts.garmin.session.Garmin")
    def test_connect_uses_file_path_fallback_directory_for_tokenstore(self, garmin_cls):
        client = garmin_cls.return_value

        with TemporaryDirectory() as tmp:
            session_file = Path(tmp) / "legacy-cookies.txt"
            session_file.write_text("cookies")

            connect(session_file=str(session_file))

            client.login.assert_called_once_with(tokenstore=f"{session_file}.session")
