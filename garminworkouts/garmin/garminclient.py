import sys

from garminworkouts.garmin.session import connect, disconnect


class GarminClient:
    _WORKOUT_SERVICE_ENDPOINT = "/proxy/workout-service"

    _REQUIRED_HEADERS = {"Referer": "https://connect.garmin.com/modern/workouts", "nk": "NT"}

    def __init__(self, connect_url, sso_url, username, password, cookie_jar):
        self.connect_url = connect_url
        self.sso_url = sso_url
        self.username = username
        self.password = password
        self.cookie_jar = cookie_jar

    def __enter__(self):
        self.session = connect(session_file=self.cookie_jar)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        disconnect(self.session)

    def list_workouts(self, batch_size=100):
        for start_index in range(0, sys.maxsize, batch_size):
            response_jsons = self.session.get_workouts(start_index, batch_size)
            if not response_jsons or response_jsons == []:
                break

            yield from response_jsons

    def get_workout(self, workout_id):
        return self.session.get_workout_by_id(workout_id)

    def download_workout(self, workout_id, file):
        content = self.session.download_workout(workout_id)

        with open(file, "wb") as f:
            f.write(content)

    def save_workout(self, workout):
        self.session.upload_workout(workout)

    def update_workout(self, workout_id, workout):
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"

        response = self.session.garth.put(url, headers=GarminClient._REQUIRED_HEADERS, json=workout)
        response.raise_for_status()

    def delete_workout(self, workout_id):
        url = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"

        response = self.session.garth.delete(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

    def schedule_workout(self, workout_id, date):
        self.session.schedule_workout(workout_id, date)
