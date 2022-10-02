import http
import json
import logging
import os
import re
import sys

import cloudscraper


class GarminClient(object):
    _SSO_LOGIN_ENDPOINT = "/sso/signin"
    _MODERN_SETTINGS_ENDPOINT = "/modern/settings"
    _WORKOUT_SERVICE_ENDPOINT = "/proxy/workout-service"

    _REQUIRED_HEADERS = {
        "Referer": "https://connect.garmin.com/modern/workouts",
        "nk": "NT"
    }

    _LOG = logging.getLogger(__name__)

    def __init__(self, connect_url, sso_url, username, password, cookie_jar):
        self.connect_url = connect_url
        self.sso_url = sso_url
        self.username = username
        self.password = password
        self.cookie_jar = cookie_jar
        self.session = None

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._disconnect()

    def list_workouts(self, batch_size=100):
        assert self.session

        for start_index in range(0, sys.maxsize, batch_size):

            url = self.connect_url + GarminClient._WORKOUT_SERVICE_ENDPOINT + "/workouts"
            params = {
                "start": start_index,
                "limit": batch_size
            }
            response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS, params=params)
            response.raise_for_status()

            response_jsons = json.loads(response.text)
            if not response_jsons or response_jsons == []:
                break

            for response_json in response_jsons:
                yield response_json

    def get_workout(self, workout_id):
        assert self.session

        url = self.connect_url + GarminClient._WORKOUT_SERVICE_ENDPOINT + "/workout/%s" % workout_id

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        return json.loads(response.text)

    def download_workout(self, workout_id, file):
        assert self.session

        url = self.connect_url + GarminClient._WORKOUT_SERVICE_ENDPOINT + "/workout/FIT/%s" % workout_id

        response = self.session.get(url)
        response.raise_for_status()

        with open(file, "wb") as f:
            f.write(response.content)

    def save_workout(self, workout):
        assert self.session

        url = self.connect_url + GarminClient._WORKOUT_SERVICE_ENDPOINT + "/workout"

        response = self.session.post(url, headers=GarminClient._REQUIRED_HEADERS, json=workout)
        response.raise_for_status()

    def update_workout(self, workout_id, workout):
        assert self.session

        url = self.connect_url + GarminClient._WORKOUT_SERVICE_ENDPOINT + "/workout/%s" % workout_id

        response = self.session.put(url, headers=GarminClient._REQUIRED_HEADERS, json=workout)
        response.raise_for_status()

    def delete_workout(self, id):
        assert self.session

        url = self.connect_url + GarminClient._WORKOUT_SERVICE_ENDPOINT + "/workout/%s" % id

        response = self.session.delete(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

    def schedule_workout(self, workout_id, date):
        assert self.session

        url = self.connect_url + GarminClient._WORKOUT_SERVICE_ENDPOINT + "/schedule/%s" % workout_id
        json_data = {"date": date}

        response = self.session.post(url, headers=GarminClient._REQUIRED_HEADERS, json=json_data)
        response.raise_for_status()

    def _connect(self):
        self.session = cloudscraper.CloudScraper()

        if self.cookie_jar:
            self.session.cookies = http.cookiejar.LWPCookieJar(self.cookie_jar)

            if os.path.isfile(self.cookie_jar):
                self.session.cookies.load(ignore_discard=True, ignore_expires=True)

        url = self.connect_url + GarminClient._MODERN_SETTINGS_ENDPOINT
        response = self.session.get(url, allow_redirects=False)
        if response.status_code != 200:
            self._LOG.info("Authenticate user '%s'", self.username)
            self._authenticate()
        else:
            self._LOG.info("User '%s' already authenticated", self.username)

    def _disconnect(self):
        if self.session:
            if self.cookie_jar:
                self.session.cookies.save(ignore_discard=True, ignore_expires=True)

            self.session.close()
            self.session = None

    def _authenticate(self):
        assert self.session

        url = self.sso_url + GarminClient._SSO_LOGIN_ENDPOINT
        headers = {'origin': 'https://sso.garmin.com'}
        params = {
            "service": "https://connect.garmin.com/modern"
        }
        data = {
            "username": self.username,
            "password": self.password,
            "embed": "false"
        }

        auth_response = self.session.post(url, headers=headers, params=params, data=data)
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
