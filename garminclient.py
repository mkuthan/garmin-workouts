import json
import re

import requests

SSO_LOGIN_URL = "https://sso.garmin.com/sso/signin"
WORKOUT_SERVICE_URL = "https://connect.garmin.com/modern/proxy/workout-service"


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

        response = self.session.get(WORKOUT_SERVICE_URL + "/workouts")
        response.raise_for_status()

        return json.loads(response.text)

    def get_workout(self, id):
        self._require_session()

        response = self.session.get(WORKOUT_SERVICE_URL + "/workout/%s" % id)
        response.raise_for_status()

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
        auth_response.raise_for_status()

        auth_ticket_url = self._extract_auth_ticket_url(auth_response.text)

        response = self.session.get(auth_ticket_url)
        response.raise_for_status()

    @staticmethod
    def _extract_auth_ticket_url(auth_response):
        match = re.search(r'response_url\s*=\s*"(https:[^"]+)"', auth_response)
        if not match:
            raise Exception("Unable to extract auth ticket URL from:\n%s" % auth_response)
        auth_ticket_url = match.group(1).replace("\\", "")
        return auth_ticket_url
