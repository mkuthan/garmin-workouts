import json
import re

import requests

SSO_LOGIN_URL = "https://sso.garmin.com/sso/signin"
WORKOUTS_URL = "https://connect.garmin.com/modern/proxy/workout-service/workouts"


class GarminClientException(Exception):
    pass


class GarminClient(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        self.session = requests.Session()
        self._authenticate()

    def disconnect(self):
        if self.session:
            self.session.close()
            self.session = None

    def list_workouts(self):
        self._require_session()

        response = self.session.get(WORKOUTS_URL)
        if response.status_code != 200:
            raise GarminClientException("Could not fetch workouts %d %s" % (response.code, response.text))

        return json.loads(response.text)

    def _require_session(self):
        if not self.session:
            raise Exception("Session is not initialized, call connect()")

    def _authenticate(self):
        form_data = {
            "username": self.username,
            "password": self.password,
            "embed": "false"
        }
        request_params = {
            "service": "https://connect.garmin.com/modern"
        }
        headers = {'origin': 'https://sso.garmin.com'}

        auth_response = self.session.post(SSO_LOGIN_URL, headers=headers, params=request_params, data=form_data)

        if auth_response.status_code != 200:
            raise GarminClientException("Authentication failure %d %s" % (auth_response.code, auth_response.text))

        auth_ticket_url = self._extract_auth_ticket_url(auth_response.text)
        response = self.session.get(auth_ticket_url)

        if response.status_code != 200:
            raise GarminClientException("Failed to claim auth ticket %d %s" % (response.status_code, response.text))

    @staticmethod
    def _extract_auth_ticket_url(auth_response):
        match = re.search(r'response_url\s*=\s*"(https:[^"]+)"', auth_response)
        if not match:
            raise GarminClientException("Unable to extract auth ticket URL from %s" % auth_response)
        auth_ticket_url = match.group(1).replace("\\", "")
        return auth_ticket_url
