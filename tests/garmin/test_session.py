import unittest

import requests
from pytest_httpserver import HTTPServer

from garminworkouts.garmin.session import connect, disconnect


class SessionTestCase(unittest.TestCase):

    def setUp(self):
        self.httpserver = HTTPServer()
        self.httpserver.start()
        self.addCleanup(self.httpserver.stop)

        self.url = f"http://{self.httpserver.host}:{self.httpserver.port}"
        self.username = "any-username"
        self.password = "any-password"

    def test_already_authenticated(self):
        self._modern_settings_request(status=200)
        self._try_connect()

    def test_authentication_succeeded(self):
        self._modern_settings_request(status=403)

        self.httpserver \
            .expect_request("/sso/signin", method="POST", data=self._signin_data()) \
            .respond_with_data('response_url = "https://connect.garmin.com/modern?ticket=any-auth-ticket"')

        self.httpserver \
            .expect_request("/modern", query_string={"ticket": "any-auth-ticket"}) \
            .respond_with_data()

        self._try_connect()

    def test_authentication_failed_wrong_ticket(self):
        self._modern_settings_request(status=403)

        self.httpserver \
            .expect_request("/sso/signin", method="POST", data=self._signin_data()) \
            .respond_with_data('response_url = "https://connect.garmin.com/modern?ticket=any-auth-ticket"')

        self.httpserver \
            .expect_request("/modern", query_string={"ticket": "any-auth-ticket"}) \
            .respond_with_data(status=403)

        with self.assertRaises(requests.exceptions.HTTPError):
            self._try_connect()

    def test_authentication_failed_unknown_ticket(self):
        self._modern_settings_request(status=403)

        self.httpserver \
            .expect_request("/sso/signin", method="POST", data=self._signin_data()) \
            .respond_with_data('response_url = "https://connect.garmin.com/modern?foo=bar"')

        with self.assertRaises(Exception):
            self._try_connect()

    def test_authentication_failed_signin(self):
        self._modern_settings_request(status=403)

        self.httpserver \
            .expect_request("/sso/signin", method="POST", data=self._signin_data()) \
            .respond_with_data(status=403)

        with self.assertRaises(requests.exceptions.HTTPError):
            self._try_connect()

    def _try_connect(self):
        session = connect(connect_url=self.url,
                          sso_url=self.url,
                          username=self.username,
                          password=self.password,
                          cookie_jar=None)
        disconnect(session)

    def _modern_settings_request(self, status):
        self.httpserver \
            .expect_request("/modern/settings") \
            .respond_with_data(status=status)

    def _signin_data(self):
        return f"username={self.username}&password={self.password}&embed=false"
