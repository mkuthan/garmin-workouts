import json
import sys
import logging
from datetime import datetime

from garminworkouts.garmin.session import connect, disconnect
from garminworkouts.models.running_workout import Workout


class GarminClient(object):
    _WORKOUT_SERVICE_ENDPOINT = "/proxy/workout-service"
    _CALENDAR_SERVICE_ENDPOINT = "/proxy/calendar-service"

    _REQUIRED_HEADERS = {
        "Referer": "https://connect.garmin.com/modern/workouts",
        "Nk": "NT"
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

    def list_types(self):
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/types"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        return json.loads(response.text)

    def external_workouts(self):
        url = f"{self.connect_url}/web-data/workouts/es-ES/index.json"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        workout_list = json.loads(response.text)
        return workout_list['workouts']

    def get_external_workout(self, code):
        url = f"{self.connect_url}/web-data/workouts/es-ES/{code}.json"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        workout = json.loads(response.text)
        return workout

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

    def download_workout_yaml(self, workout_id, filename):
        Workout.export_yaml(self.get_workout(workout_id), filename)

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

    def get_calendar(self, date):
        year = str(date.year)
        month = str(date.month - 1)
        url = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        response_jsons = json.loads(response.text)

        for item in response_jsons['calendarItems']:
            if datetime.strptime(item['date'], '%Y-%m-%d').date() < date and item['itemType'] == 'workout':
                print(item['title'], item['date'], item['id'], item['itemType'])
                logging.info("Deleting workout '%s'", item['title'])
                self.delete_workout(item['id'])

    def schedule_workout(self, workout_id, date):
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data = {"date": date}

        response = self.session.post(url, headers=GarminClient._REQUIRED_HEADERS, json=json_data)
        response.raise_for_status()

    def remove_workout(self, workout_id, date):
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data = {"date": date}

        response = self.session.delete(url, headers=GarminClient._REQUIRED_HEADERS, json=json_data)
        response.raise_for_status()

    def list_events(self, batch_size=20):
        for start_index in range(1, sys.maxsize, batch_size):
            url = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/events"
            params = {
                "startDate": datetime.today(),
                "pageIndex": start_index,
                "limit": batch_size
            }
            response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS, params=params)
            response.raise_for_status()

            response_jsons = json.loads(response.text)
            if not response_jsons or response_jsons == []:
                break

            for response_json in response_jsons:
                yield response_json

    def get_event(self, event_id):
        url = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        return json.loads(response.text)

    def save_event(self, event):
        url = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event"

        response = self.session.post(url, headers=GarminClient._REQUIRED_HEADERS, json=event)
        response.raise_for_status()

    def update_event(self, event_id, event):
        url = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"

        response = self.session.put(url, headers=GarminClient._REQUIRED_HEADERS, json=event)
        response.raise_for_status()

    def delete_event(self, event_id):
        url = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"

        response = self.session.delete(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()
