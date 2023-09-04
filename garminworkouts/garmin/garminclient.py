import json
import sys
import logging
from datetime import datetime, date

from garminworkouts.garmin.session import connect, disconnect
from garminworkouts.models.extraction import export_yaml


class GarminClient(object):
    _WORKOUT_SERVICE_ENDPOINT = "/proxy/workout-service"
    _CALENDAR_SERVICE_ENDPOINT = "/proxy/calendar-service"
    _ACTIVITY_SERVICE_ENDPOINT = "/proxy/activity-service"
    _BIOMETRIC_SERVICE_ENDPOINT = "/proxy/biometric-service"
    _WELLNESS_SERVICE_ENDPOINT = "/proxy/wellness-service"
    _ACTIVITY_LIST_SERVICE_ENDPOINT = "/proxy/activitylist-service"
    _TRAINING_PLAN_SERVICE_ENDPOINT = "/proxy/trainingplan-service/trainingplan"
    _GOLF_COMMUNITY_ENDPOINT = "/proxy/gcs-golfcommunity/api/v2/club"

    _REQUIRED_HEADERS: dict[str, str] = {
        "Referer": "https://connect.garmin.com/modern/workouts",
        "Nk": "NT"
    }

    def __init__(self, connect_url, sso_url, username, password, cookie_jar) -> None:
        self.connect_url: str = connect_url
        self.sso_url: str = sso_url
        self.username: str = username
        self.password: str = password
        self.cookie_jar = cookie_jar

    def __enter__(self):
        if isinstance(self.connect_url, tuple):
            self.connect_url = ''.join(self.connect_url)
        if isinstance(self.sso_url, tuple):
            self.sso_url = ''.join(self.sso_url)
        if isinstance(self.cookie_jar, tuple):
            self.cookie_jar: str = ''.join(self.sso_url)

        self.session = connect(self.connect_url, self.sso_url, self.username, self.password, self.cookie_jar)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        disconnect(self.session)

    def list_types(self) -> dict:
        url: str = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/types"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        return json.loads(response.text)

    def external_workouts(self, locale) -> dict:
        url: str = f"{self.connect_url}/web-data/workouts/{locale}/index.json"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        workout_list: dict = json.loads(response.text)
        return workout_list['workouts']

    def get_external_workout(self, code, locale) -> dict:
        url: str = f"{self.connect_url}/web-data/workouts/{locale}/{code}.json"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        workout: dict = json.loads(response.text)
        return workout

    def list_workouts(self, batch_size=100):
        for start_index in range(0, sys.maxsize, batch_size):

            url: str = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workouts"
            params: dict[str, int] = {
                "start": start_index,
                "limit": batch_size
            }
            response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS, params=params)
            response.raise_for_status()

            response_jsons: dict = json.loads(response.text)
            if not response_jsons or response_jsons == []:
                break

            for response_json in response_jsons:
                yield response_json

    def get_workout(self, workout_id) -> dict:
        url: str = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        return json.loads(response.text)

    def download_workout_yaml(self, workout_id, filename) -> None:
        export_yaml(self.get_workout(workout_id), filename)

    def download_workout(self, workout_id, file) -> None:
        url: str = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/FIT/{workout_id}"

        response = self.session.get(url)
        response.raise_for_status()

        with open(file, "wb") as f:
            f.write(response.content)

    def save_workout(self, workout) -> None:
        url: str = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout"

        response = self.session.post(url, headers=GarminClient._REQUIRED_HEADERS, json=workout)
        response.raise_for_status()

    def update_workout(self, workout_id, workout) -> None:
        url: str = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"

        response = self.session.put(url, headers=GarminClient._REQUIRED_HEADERS, json=workout)
        response.raise_for_status()

    def delete_workout(self, workout_id) -> None:
        url: str = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"

        response = self.session.delete(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

    def get_calendar(self, date) -> None:
        year = str(date.year)
        month = str(date.month - 1)
        url: str = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        response_jsons: dict = json.loads(response.text)

        for item in response_jsons['calendarItems']:
            if datetime.strptime(item['date'], '%Y-%m-%d').date() < date and item['itemType'] == 'workout':
                logging.info("Deleting workout '%s'", item['title'])
                self.delete_workout(item['workoutId'])

    def schedule_workout(self, workout_id, date) -> None:
        url: str = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data: dict = {"date": date}

        response = self.session.post(url, headers=GarminClient._REQUIRED_HEADERS, json=json_data)
        response.raise_for_status()

    def remove_workout(self, workout_id, date) -> None:
        url: str = f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data: dict = {"date": date}

        response = self.session.delete(url, headers=GarminClient._REQUIRED_HEADERS, json=json_data)
        response.raise_for_status()

    def list_events(self, batch_size=20):
        for start_index in range(1, sys.maxsize, batch_size):
            url: str = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/events"
            params: dict = {
                "startDate": datetime.today(),
                "pageIndex": start_index,
                "limit": batch_size
            }
            response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS, params=params)
            response.raise_for_status()

            response_jsons: dict = json.loads(response.text)
            if not response_jsons or response_jsons == []:
                break

            for response_json in response_jsons:
                yield response_json

    def get_event(self, event_id) -> dict:
        url: str = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        return json.loads(response.text)

    def save_event(self, event) -> None:
        url: str = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event"

        response = self.session.post(url, headers=GarminClient._REQUIRED_HEADERS, json=event)
        response.raise_for_status()

    def update_event(self, event_id, event) -> None:
        url: str = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"

        response = self.session.put(url, headers=GarminClient._REQUIRED_HEADERS, json=event)
        response.raise_for_status()

    def delete_event(self, event_id) -> None:
        url: str = f"{self.connect_url}{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"

        response = self.session.delete(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

    def get_activities_by_date(self, startdate, enddate, activitytype=None) -> list:
        """
        Fetch available activities between specific dates
        :param startdate: String in the format YYYY-MM-DD
        :param enddate: String in the format YYYY-MM-DD
        :param activitytype: (Optional) Type of activity you are searching
                             Possible values are [cycling, running, swimming,
                             multi_sport, fitness_equipment, hiking, walking, other]
        :return: list of JSON activities
        """

        activities: list = []
        start = 0
        limit = 20
        # mimicking the behavior of the web interface that fetches 20 activities at a time
        # and automatically loads more on scroll
        url: str = f"{self.connect_url}{GarminClient._ACTIVITY_LIST_SERVICE_ENDPOINT}/activities/search/activities"
        params: dict[str, str] = {
            "startDate": str(startdate),
            "endDate": str(enddate),
            "start": str(start),
            "limit": str(limit),
        }
        if activitytype:
            params["activityType"] = str(activitytype)

        print(f"Requesting activities by date from {startdate} to {enddate}")
        while True:
            params["start"] = str(start)
            print(f"Requesting activities {start} to {start+limit}")
            act = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS, params=params).json()
            if act:
                activities.extend(act)
                start = start + limit
            else:
                break

        return activities

    def list_trainingplans(self, locale) -> dict:
        url: str = f"{self.connect_url}{self._TRAINING_PLAN_SERVICE_ENDPOINT}/search"
        params: dict = {
            "start": '1',
            "limit": '1000',
            "locale": locale.split('-')[0],
        }

        response = self.session.post(url, headers=GarminClient._REQUIRED_HEADERS, params=params)
        response.raise_for_status()

        return json.loads(response.text)['trainingPlanList']

    def schedule_training_plan(self, plan_id, startDate) -> dict:
        url: str = f"{self.connect_url}{self._TRAINING_PLAN_SERVICE_ENDPOINT}/schedule/{plan_id}"
        params: dict = {
            "startDate": startDate,
        }

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS, params=params)
        response.raise_for_status()

        return json.loads(response.text)

    def get_training_plan(self, plan_id, locale) -> dict:
        url: str = f"{self.connect_url}{self._TRAINING_PLAN_SERVICE_ENDPOINT}/tasks/{plan_id}"
        params: dict = {
            "localeKey": locale,
        }

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS, params=params)
        response.raise_for_status()

        return json.loads(response.text)

    def delete_training_plan(self, plan_id) -> None:
        url = f"{self.connect_url}{self._TRAINING_PLAN_SERVICE_ENDPOINT}/trainingplan/{plan_id}"

        response = self.session.delete(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

    def get_types(self) -> None:
        url: str = f"{self.connect_url}{self._WORKOUT_SERVICE_ENDPOINT}/workout/types"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        sec = {}
        for type in json.loads(response.text)['workoutSportTypes']:
            sec.update({type['sportTypeKey']: type['sportTypeId']})
        print('SPORT_TYPES =', sec, '\n')

        sec = {}
        for type in json.loads(response.text)['workoutIntensityTypes']:
            sec.update({type['intensityTypeKey']: type['intensityTypeId']})
        print('INTENSITY_TYPES =', sec, '\n')

        sec = {}
        for type in json.loads(response.text)['workoutStepTypes']:
            sec.update({type['stepTypeKey']: type['stepTypeId']})
        print('STEP_TYPES =', sec, '\n')

        sec = {}
        for type in json.loads(response.text)['workoutConditionTypes']:
            sec.update({type['conditionTypeKey']: type['conditionTypeId']})
        print('END_CONDITIONS = ', sec, '\n')

        sec = {}
        for type in json.loads(response.text)['workoutTargetTypes']:
            sec.update({type['workoutTargetTypeKey']: type['workoutTargetTypeId']})
        print('TARGET_TYPES = ', sec, '\n')

        sec = {}
        for type in json.loads(response.text)['workoutEquipmentTypes']:
            sec.update({type['equipmentTypeKey']: type['equipmentTypeId']})
        print('EQUIPMENT_TYPES = ', sec, '\n')

        sec: dict = {}
        for type in json.loads(response.text)['workoutStrokeTypes']:
            sec.update({type['strokeTypeKey']: type['strokeTypeId']})
        print('STROKE_TYPES = ', sec, '\n')

        self.get_activity_types()
        self.get_event_types()
        self.get_golf_types()
        self.get_strength_types()

    def get_activity_types(self) -> None:
        url: str = f"{self.connect_url}{self._ACTIVITY_SERVICE_ENDPOINT}/activity/activityTypes"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        sec: dict = {}
        for type in json.loads(response.text):
            sec.update({type['typeKey']: type['typeId']})
        print('ACTIVITY_TYPES = ', sec, '\n')

    def get_event_types(self) -> None:
        url: str = f"{self.connect_url}{self._ACTIVITY_SERVICE_ENDPOINT}/activity/eventTypes"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        sec: dict = {}

        for type in json.loads(response.text):
            sec.update({type['typeKey']: type['typeId']})
        print('EVENT_TYPES = ', sec, '\n')

    def get_golf_types(self) -> None:
        url = f"{self.connect_url}{self._GOLF_COMMUNITY_ENDPOINT}/types"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        sec = {}
        for type in json.loads(response.text):
            sec.update({type['name']: type['value']})
        print('GOLF_CLUB = ', sec, '\n')

        url: str = f"{self.connect_url}{self._GOLF_COMMUNITY_ENDPOINT}/flex-types"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        sec: dict = {}
        for type in json.loads(response.text):
            sec.update({type['name']: type['id']})
        print('GOLF_FLEX = ', sec, '\n')

    def get_strength_types(self) -> None:
        url: str = f"{self.connect_url}/web-data/exercises/Exercises.json"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        sec: dict = json.loads(response.text)
        with open(".\\garminworkouts\\models\\strength.py", "w") as fp:
            json.dump(sec, fp)  # encode dict into JSON

    def get_RHR(self) -> int:
        url: str = f"{self.connect_url}{self._WELLNESS_SERVICE_ENDPOINT}/wellness/dailyHeartRate"
        params: dict = {
            "date": date.today(),
        }

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS, params=params)
        response.raise_for_status()

        a: dict = json.loads(response.text)
        return int(a['restingHeartRate'])

    def get_hr_zones(self) -> dict:
        url: str = f"{self.connect_url}{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS,)
        response.raise_for_status()

        return json.loads(response.text)

    def save_hr_zones(self, zones) -> None:
        url: str = f"{self.connect_url}{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"

        response = self.session.put(url, headers=GarminClient._REQUIRED_HEADERS, json=zones)
        response.raise_for_status()

    def get_power_zones(self):
        url: str = f"{self.connect_url}{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/sports/all"

        response = self.session.get(url, headers=GarminClient._REQUIRED_HEADERS)
        response.raise_for_status()

        return json.loads(response.text)
