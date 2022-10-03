import json
import sys

from garminworkouts.garmin.session import connect, disconnect


class GarminClient(object):
    _WORKOUT_SERVICE_ENDPOINT = "/proxy/workout-service"

    _REQUIRED_HEADERS = {
        "Referer": "https://connect.garmin.com/modern/workouts",
        "nk": "NT"
    }

    def __init__(self, connect_url, sso_url, username, password, cookie_jar):
        self.connect_url = connect_url
        self.sso_url = sso_url
        self.username = username
        self.password = password
        self.cookie_jar = cookie_jar

    def __enter__(self):
        self.session = connect(self.connect_url, self.sso_url, self.username, self.password, self.cookie_jar)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        disconnect(self.session)

    def list_workouts(self, batch_size=100):
        for start_index in range(0, sys.maxsize, batch_size):

            url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workouts"
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
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        return json.loads(response.text)

    def download_workout(self, workout_id, file):
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/FIT/{workout_id}"

        response = self.session.get(url)
        response.raise_for_status()

        with open(file, "wb") as f:
            f.write(response.content)

    def save_workout(self, workout):
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout"

        response = self.session.post(url, headers=GarminClient._REQUIRED_HEADERS, json=workout)
        response.raise_for_status()

    def update_workout(self, workout_id, workout):
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"

        response = self.session.put(url, headers=GarminClient._REQUIRED_HEADERS, json=workout)
        response.raise_for_status()

    def delete_workout(self, workout_id):
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"

        response = self.session.delete(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

    def schedule_workout(self, workout_id, date):
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data = {"date": date}

        response = self.session.post(url, headers=GarminClient._REQUIRED_HEADERS, json=json_data)
        response.raise_for_status()
