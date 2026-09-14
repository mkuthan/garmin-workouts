import sys
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from garminworkouts import __main__ as main_module
from garminworkouts.garmin.session import SessionLoginRequiredError


class MainTestCase(TestCase):
    @patch("garminworkouts.__main__.session_login")
    def test_command_login_calls_session_login(self, session_login_mock):
        args = SimpleNamespace(username="user", password="pass", cookie_jar="/tmp/session")

        main_module.command_login(args)

        session_login_mock.assert_called_once_with(username="user", password="pass", session_file="/tmp/session")

    @patch("garminworkouts.__main__.session_login")
    @patch("garminworkouts.__main__.getpass.getpass", return_value="prompted-pass")
    @patch("garminworkouts.__main__.input", return_value="prompted-user")
    def test_command_login_prompts_for_missing_credentials(self, input_mock, getpass_mock, session_login_mock):
        args = SimpleNamespace(username=None, password=None, cookie_jar="/tmp/session")

        main_module.command_login(args)

        input_mock.assert_called_once_with("Garmin username: ")
        getpass_mock.assert_called_once_with("Garmin password: ")
        session_login_mock.assert_called_once_with(
            username="prompted-user",
            password="prompted-pass",
            session_file="/tmp/session",
        )

    @patch("garminworkouts.__main__.GarminClient")
    def test_garmin_client_allows_missing_credentials(self, garmin_client_cls):
        args = SimpleNamespace(
            connect_url="https://connect.garmin.com",
            sso_url="https://sso.garmin.com",
            username=None,
            password=None,
            cookie_jar="/tmp/session",
        )

        main_module._garmin_client(args)

        garmin_client_cls.assert_called_once_with(
            connect_url="https://connect.garmin.com",
            sso_url="https://sso.garmin.com",
            username=None,
            password=None,
            cookie_jar="/tmp/session",
        )

    @patch("garminworkouts.__main__.session_login")
    @patch("garminworkouts.__main__.logging.error")
    def test_main_catches_login_required_error_and_exits_1(self, log_error_mock, session_login_mock):
        session_login_mock.side_effect = SessionLoginRequiredError("need login")

        with patch.object(sys, "argv", ["garmin-workouts", "--username", "user", "--password", "pass", "login"]):
            with self.assertRaises(SystemExit) as context:
                main_module.main()

        self.assertEqual(context.exception.code, 1)
        log_error_mock.assert_called_once_with("need login")

    @patch("garminworkouts.__main__.session_login")
    @patch("garminworkouts.__main__.getpass.getpass", return_value="prompted-pass")
    @patch("garminworkouts.__main__.input", return_value="prompted-user")
    def test_main_login_prompts_when_credentials_missing(self, input_mock, getpass_mock, session_login_mock):
        with patch.object(sys, "argv", ["garmin-workouts", "login"]):
            main_module.main()

        input_mock.assert_called_once_with("Garmin username: ")
        getpass_mock.assert_called_once_with("Garmin password: ")
        session_login_mock.assert_called_once_with(
            username="prompted-user",
            password="prompted-pass",
            session_file=".garmin-session",
        )
