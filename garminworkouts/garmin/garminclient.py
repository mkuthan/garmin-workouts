import json
import sys
import logging
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional
from garminworkouts.garmin.session import connect, disconnect
from garminworkouts.models.extraction import export_yaml
import garth
import os


class GarminClient(object):
    _WORKOUT_SERVICE_ENDPOINT = "/workout-service"
    _CALENDAR_SERVICE_ENDPOINT = "/calendar-service"
    _ACTIVITY_SERVICE_ENDPOINT = "/activity-service"
    _BIOMETRIC_SERVICE_ENDPOINT = "/biometric-service"
    _WELLNESS_SERVICE_ENDPOINT = "/wellness-service"
    _ACTIVITY_LIST_SERVICE_ENDPOINT = "/activitylist-service"
    _TRAINING_PLAN_SERVICE_ENDPOINT = "/trainingplan-service/trainingplan"
    _GOLF_COMMUNITY_ENDPOINT = "/gcs-golfcommunity/api/v2/club"

    def __init__(self, connect_url, sso_url, username, password, cookie_jar, is_cn=False, tokenstore=None) -> None:
        self.connect_url: str = connect_url
        self.sso_url: str = sso_url
        self.username: str = username
        self.password: str = password
        self.cookie_jar = cookie_jar

        self.garth = garth.Client(
            domain="garmin.cn" if is_cn else "garmin.com"
        )

        """Log in using Garth."""
        tokenstore = tokenstore or os.getenv("GARMINTOKENS")

        if tokenstore:
            self.garth.load(tokenstore)
        else:
            self.garth.login(self.username, self.password)
            # Save tokens for next login
            self.garth.dump(tokenstore)

        self.display_name = self.garth.profile["displayName"]
        self.full_name = self.garth.profile["fullName"]

        settings = self.garth.connectapi(
            "/userprofile-service/userprofile/user-settings"
        )
        self.unit_system = settings["userData"]["measurementSystem"] if settings is not None else None

        self.display_name = None
        self.full_name = None
        self.unit_system = None

    def connectapi(self, path, **kwargs):
        return self.garth.connectapi(path, **kwargs)

    def download(self, path, **kwargs):
        return self.garth.download(path, **kwargs)

    def login(self, /, tokenstore: Optional[str] = None):
        """Log in using Garth."""
        tokenstore = tokenstore or os.getenv("GARMINTOKENS")

        if tokenstore:
            self.garth.load(tokenstore)
        else:
            self.garth.login(self.username, self.password)

        self.display_name = self.garth.profile["displayName"]
        self.full_name = self.garth.profile["fullName"]

        settings = self.garth.connectapi(
            "/userprofile-service/userprofile/user-settings"
        )
        self.unit_system = settings["userData"]["measurementSystem"] if settings is not None else None

        return True

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

    def list_types(self):
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/types"
        return self.connectapi(url)

    def external_workouts(self, locale):
        url: str = f"web-data/workouts/{locale}/index.json"
        workout_list = self.connectapi(url)

        return workout_list['workouts'] if workout_list is not None else None

    def get_external_workout(self, code, locale):
        url: str = f"web-data/workouts/{locale}/{code}.json"
        return self.connectapi(url)

    def list_workouts(self, batch_size=100):
        for start_index in range(0, sys.maxsize, batch_size):
            url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workouts"

            params: dict[str, int] = {
                "start": start_index,
                "limit": batch_size
            }
            response_jsons = self.connectapi(url, params=params)

            if not response_jsons or response_jsons == []:
                break

            for response_json in response_jsons:
                yield response_json

    def get_workout(self, workout_id):
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        return self.connectapi(url)

    def download_workout_yaml(self, workout_id, filename) -> None:
        export_yaml(self.get_workout(workout_id), filename)

    def download_workout(self, workout_id, file) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/FIT/{workout_id}"
        response = self.connectapi(url)

        with open(file, "wb") as f:
            f.write(response)

    def save_workout(self, workout) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout"
        self.connectapi(url, json=workout)

    def update_workout(self, workout_id, workout) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        self.garth.put("connectapi", url, json=workout)

    def delete_workout(self, workout_id) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        self.connectapi(url)

    def get_calendar(self, date, days) -> list:
        year = str(date.year)
        month = str(date.month - 1)
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}"

        response = self.connectapi(url)

        response_jsons = response if response is not None else None

        updateable_elements = []
        for item in response_jsons['calendarItems']:
            if item['itemType'] == 'workout':
                if datetime.strptime(item['date'], '%Y-%m-%d').date() < date:
                    logging.info("Deleting workout '%s'", item['title'])
                    self.delete_workout(item['workoutId'])
                elif datetime.strptime(item['date'], '%Y-%m-%d').date() < date + timedelta(days=days):
                    updateable_elements.append(item['title'])

        return updateable_elements

    def schedule_workout(self, workout_id, date) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data: dict = {"date": date}

        self.garth.post(url, json=json_data)

    def remove_workout(self, workout_id, date) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data: dict = {"date": date}

        response = self.garth.delete(url, json=json_data)
        response.raise_for_status()

    def list_events(self, batch_size=20):
        for start_index in range(1, sys.maxsize, batch_size):
            url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/events"
            params: dict = {
                "startDate": datetime.today(),
                "pageIndex": start_index,
                "limit": batch_size
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()

            response_jsons: dict = json.loads(response.text)
            if not response_jsons or response_jsons == []:
                break

            for response_json in response_jsons:
                yield response_json

    def get_event(self, event_id):
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"

        return self.garth.connectapi(url)

    def save_event(self, event) -> None:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event"

        self.garth.post(url, json=event)

    def update_event(self, event_id, event) -> None:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"

        self.garth.put("connectapi", url, json=event)

    def delete_event(self, event_id) -> None:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"

        response = self.session.delete(url)
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
        url: str = f"{GarminClient._ACTIVITY_LIST_SERVICE_ENDPOINT}/activities/search/activities"
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
            act = self.garth.connectapi(url, params=params)
            if act:
                activities.extend(act)
                start = start + limit
            else:
                break

        return activities

    def list_trainingplans(self, locale) -> dict:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/search"
        params: dict = {
            "start": '1',
            "limit": '1000',
            "locale": locale.split('-')[0],
        }

        response = self.garth.post(url, params=params)

        return json.loads(response.text)['trainingPlanList']

    def schedule_training_plan(self, plan_id, startDate):
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/schedule/{plan_id}"
        params: dict = {
            "startDate": startDate,
        }

        return self.garth.connectapi(url, params=params)

    def get_training_plan(self, plan_id, locale):
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/tasks/{plan_id}"
        params: dict = {
            "localeKey": locale,
        }

        return self.garth.connectapi(url, params=params)

    def delete_training_plan(self, plan_id) -> None:
        url = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/trainingplan/{plan_id}"

        response = self.garth.delete("connectapi", url)

    def get_types(self) -> None:
        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workout/types"

        response = self.session.get(url)
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
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/activityTypes"

        response = self.session.get(url,)
        response.raise_for_status()

        sec: dict = {}
        for type in json.loads(response.text):
            sec.update({type['typeKey']: type['typeId']})
        print('ACTIVITY_TYPES = ', sec, '\n')

    def get_event_types(self) -> None:
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/eventTypes"

        response = self.session.get(url,)
        response.raise_for_status()

        sec: dict = {}

        for type in json.loads(response.text):
            sec.update({type['typeKey']: type['typeId']})
        print('EVENT_TYPES = ', sec, '\n')

    def get_golf_types(self) -> None:
        url = f"{self._GOLF_COMMUNITY_ENDPOINT}/types"

        response = self.session.get(url,)
        response.raise_for_status()

        sec = {}
        for type in json.loads(response.text):
            sec.update({type['name']: type['value']})
        print('GOLF_CLUB = ', sec, '\n')

        url: str = f"{self._GOLF_COMMUNITY_ENDPOINT}/flex-types"

        response = self.session.get(url,)
        response.raise_for_status()

        sec: dict = {}
        for type in json.loads(response.text):
            sec.update({type['name']: type['id']})
        print('GOLF_FLEX = ', sec, '\n')

    def get_strength_types(self) -> None:
        url: str = "/web-data/exercises/Exercises.json"

        response = self.session.get(url,)
        response.raise_for_status()

        sec: dict = json.loads(response.text)
        with open(".\\garminworkouts\\models\\strength.py", "w") as fp:
            json.dump(sec, fp)  # encode dict into JSON

    def get_RHR(self) -> int:
        url: str = f"{self._WELLNESS_SERVICE_ENDPOINT}/wellness/dailyHeartRate"
        params: dict = {
            "date": date.today(),
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()

        a: dict = json.loads(response.text)
        return int(a['restingHeartRate'])

    def get_hr_zones(self):
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"

        return self.garth.connectapi(url)

    def save_hr_zones(self, zones) -> None:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"

        response = self.session.put(url, json=zones)
        response.raise_for_status()

    def get_power_zones(self) -> dict:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/sports/all"

        response = self.session.get(url,)
        response.raise_for_status()

        return json.loads(response.text)

    def save_power_zones(self, zones) -> None:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/all"

        response = self.session.put(url, json=zones)
        response.raise_for_status()
