import json
import sys
import logging
from datetime import datetime, date, timedelta
from requests import Response
from typing import Any, Literal, Generator, Optional
from garminworkouts.models.extraction import workout_export_yaml
import garth
import os
from garminworkouts.models.trainingplan_list import trainingplan_list
from garth.exc import GarthHTTPError


class GarminClient(object):
    _GARMIN_SUBDOMAIN = "connectapi"
    _GARMIN_VERSION = "24.3.1.0"
    _WORKOUT_SERVICE_ENDPOINT = "/workout-service"
    _CALENDAR_SERVICE_ENDPOINT = "/calendar-service"
    _ACTIVITY_SERVICE_ENDPOINT = "/activity-service"
    _BIOMETRIC_SERVICE_ENDPOINT = "/biometric-service"
    _WELLNESS_SERVICE_ENDPOINT = "/wellness-service"
    _ACTIVITY_LIST_SERVICE_ENDPOINT = "/activitylist-service"
    _TRAINING_PLAN_SERVICE_ENDPOINT = "/trainingplan-service/trainingplan"
    _GOLF_COMMUNITY_ENDPOINT = "/gcs-golfcommunity/api/v2/club"

    def __init__(self, username, password) -> None:
        self.username: str = username
        self.password: str = password

        tokenstore: Literal['./garminconnect'] | None = "./garminconnect" if os.path.isdir("./garminconnect") else None
        self.login(tokenstore)

    def login(self, /, tokenstore: Optional[str] = None) -> Literal[True]:
        is_cn = False
        self.garth = garth.Client(
            domain="garmin.cn" if is_cn else "garmin.com"
        )
        """Log in using Garth."""
        if tokenstore:
            self.garth.load(tokenstore)
        else:
            self.garth.login(self.username, self.password)
            # Save tokens for next login
            self.garth.dump("./garminconnect")

        self.display_name: str = self.garth.profile["displayName"]
        self.full_name: str = self.garth.profile["fullName"]

        settings: Any = self.get("/userprofile-service/userprofile/user-settings").json()
        self.unit_system: Any = settings["userData"]["measurementSystem"] if settings is not None else None

        self.version: Any = self.get("/info-service/api/system/release-system").json()[0]['version']
        try:
            assert self.version == GarminClient._GARMIN_VERSION
        except AssertionError:
            logging.error('Updated version: ' + self.version + ' from ' + GarminClient._GARMIN_VERSION)

        return True

    def get(self, *args, **kwargs) -> Response:
        return self.garth.get(GarminClient._GARMIN_SUBDOMAIN, *args, **kwargs)

    def put(self, *args, **kwargs) -> Response:
        return self.garth.put(GarminClient._GARMIN_SUBDOMAIN, *args, **kwargs)

    def post(self, *args, **kwargs) -> Response:
        return self.garth.post(GarminClient._GARMIN_SUBDOMAIN, *args, **kwargs)

    def delete(self, *args, **kwargs) -> Response:
        return self.garth.delete(GarminClient._GARMIN_SUBDOMAIN, *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None

    def external_workouts(self, locale) -> Any:
        url: str = f"web-data/workouts/{locale}/index_04_2022_d6f4482b-f983-4e55-9d8d-0061e160abe7.json"
        return self.garth.get("connect", url).json()['workouts']

    def get_external_workout(self, code, locale) -> Any:
        url: str = f"web-data/workouts/{locale}/{code}.json"
        return self.garth.get("connect", url).json()

    def list_workouts(self, batch_size=100) -> Generator[Any, Any, None]:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workouts"
        for start_index in range(0, sys.maxsize, batch_size):
            params = {
                "start": start_index,
                "limit": batch_size,
                "myWorkoutsOnly": False,
                "sharedWorkoutsOnly": False,
                "orderBy": "WORKOUT_NAME",
                "orderSeq": "ASC",
                "includeAtp": True
            }
            response_jsons: Any = self.get(url, params=params).json()
            if not response_jsons or response_jsons == []:
                break
            for response_json in response_jsons:
                yield response_json

    def get_workout(self, workout_id) -> Any:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        return self.get(url).json()

    def download_workout_yaml(self, workout_id, filename) -> None:
        workout_export_yaml(self.get_workout(workout_id), filename)

    def download_workout(self, workout_id, file) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/FIT/{workout_id}"
        response = self.get(url).json()

        with open(file, "wb") as f:
            f.write(response)

    def save_workout(self, workout) -> Any:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout"
        return self.post(url, json=workout).json()

    def update_workout(self, workout_id, workout) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        self.put(url, json=workout)

    def delete_workout(self, workout_id) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        self.delete(url)

    def get_calendar(self, date, days) -> tuple[list[Any], list[Any]]:
        year = str(date.year)
        month = str(date.month - 1)
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}"

        response_jsons: Any = self.get(url).json()['calendarItems']

        updateable_elements: list[Any] = []
        checkable_elements: list[Any] = []
        for item in response_jsons:
            if item['itemType'] == 'workout':
                if datetime.strptime(item['date'], '%Y-%m-%d').date() < date:
                    logging.info("Deleting workout '%s'", item['title'])
                    self.delete_workout(item['workoutId'])
                elif datetime.strptime(item['date'], '%Y-%m-%d').date() < date + timedelta(days=days):
                    updateable_elements.append(item['title'])
            elif item['itemType'] == 'activity':
                payload = self.get_activity_workout(item['id'])
                if 'workoutName' in payload:
                    checkable_elements.append(payload['workoutName'])

        return updateable_elements, checkable_elements

    def schedule_workout(self, workout_id, date) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data: dict = {"date": date}
        self.post(url, json=json_data)

    def remove_workout(self, workout_id, date) -> None:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data: dict = {"date": date}
        self.delete(url, json=json_data)

    def list_events(self, batch_size=20) -> Generator[Any, Any, None]:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/events"
        for start_index in range(1, sys.maxsize, batch_size):
            params: dict = {
                "startDate": datetime.today(),
                "pageIndex": start_index,
                "limit": batch_size
            }
            response: Any = self.get(url, params=params).json()

            if not response or response == []:
                break

            for response_json in response:
                yield response_json

    def get_event(self, event_id) -> Any:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"
        return self.get(url).json()

    def save_event(self, event) -> Any:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event"
        return self.post(url, json=event).json()

    def update_event(self, event_id, event) -> None:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"
        self.put(url, json=event)

    def delete_event(self, event_id) -> None:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"
        self.delete(url)

    def get_activity_workout(self, activity_id) -> Any:
        url = f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/{activity_id}/workouts"
        return self.get(url).json()

    def get_activities_by_date(self,
                               startdate=None, enddate=None,
                               activitytype=None,
                               minDistance=None, maxDistance=None,  # meters
                               minDuration=None, maxDuration=None,  # seconds
                               minElevation=None, maxElevation=None,  # meters
                               ) -> list[Any]:
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

        params = {
            "startDate": str(startdate) if startdate else None,
            "endDate": str(enddate) if enddate else None,
            "start": str(start),
            "limit": str(limit),
            "activityType": str(activitytype) if activitytype else None,
            "minDistance": int(minDistance) if minDistance else None,
            "maxDistance": int(maxDistance) if maxDistance else None,
            "minDuration": int(minDuration) if minDuration else None,
            "maxDuration": int(maxDuration) if maxDuration else None,
            "minElevation": int(minElevation) if minElevation else None,
            "maxElevation": int(maxElevation) if maxElevation else None,
        }

        print(f"Requesting activities by date from {startdate} to {enddate}")
        while True:
            params["start"] = str(start)
            print(f"Requesting activities {start} to {start+limit}")
            act: Response = self.get(url, params=params).json()
            if act:
                activities.extend(act)
                start: int = start + limit
            else:
                break

        return activities

    def list_trainingplans(self, locale) -> Any:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/search"
        params: dict = {
            "start": '1',
            "limit": '1000',
            "locale": locale.split('-')[0],
        }
        try:
            return self.post(url, params=params, api=True).json()['trainingPlanList']
        except GarthHTTPError:
            print('Harcoded version used')
            return trainingplan_list['trainingPlanList']

    def schedule_training_plan(self, plan_id, startDate) -> Any:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/schedule/{plan_id}"
        params: dict = {
            "startDate": startDate,
        }
        return self.get(url, params=params).json()

    def get_training_plan(self, plan_id, locale) -> Any:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/tasks/{plan_id}"
        params: dict = {
            "localeKey": locale,
        }
        return self.get(url, params=params).json()

    def delete_training_plan(self, plan_id) -> None:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/trainingplan/{plan_id}"
        self.delete(url)

    def get_types(self) -> None:
        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workout/types"
        response: Any = self.get(url).json()

        sec = {}
        for type in response['workoutSportTypes']:
            sec.update({type['sportTypeKey']: type['sportTypeId']})
        print('SPORT_TYPES =', sec, '\n')

        sec = {}
        for type in response['workoutIntensityTypes']:
            sec.update({type['intensityTypeKey']: type['intensityTypeId']})
        print('INTENSITY_TYPES =', sec, '\n')

        sec = {}
        for type in response['workoutStepTypes']:
            sec.update({type['stepTypeKey']: type['stepTypeId']})
        print('STEP_TYPES =', sec, '\n')

        sec = {}
        for type in response['workoutConditionTypes']:
            sec.update({type['conditionTypeKey']: type['conditionTypeId']})
        print('END_CONDITIONS = ', sec, '\n')

        sec = {}
        for type in response['workoutTargetTypes']:
            sec.update({type['workoutTargetTypeKey']: type['workoutTargetTypeId']})
        print('TARGET_TYPES = ', sec, '\n')

        sec = {}
        for type in response['workoutEquipmentTypes']:
            sec.update({type['equipmentTypeKey']: type['equipmentTypeId']})
        print('EQUIPMENT_TYPES = ', sec, '\n')

        sec: dict = {}
        for type in response['workoutStrokeTypes']:
            sec.update({type['strokeTypeKey']: type['strokeTypeId']})
        print('STROKE_TYPES = ', sec, '\n')

        self.get_activity_types()
        self.get_event_types()
        self.get_golf_types()
        self.get_strength_types()

    def get_activity_types(self) -> None:
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/activityTypes"
        response: Any = self.get(url).json()

        sec: dict = {}
        for type in response:
            sec.update({type['typeKey']: type['typeId']})
        print('ACTIVITY_TYPES = ', sec, '\n')

    def get_event_types(self) -> None:
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/eventTypes"
        response: Any = self.get(url).json()

        sec: dict = {}

        for type in response:
            sec.update({type['typeKey']: type['typeId']})
        print('EVENT_TYPES = ', sec, '\n')

    def get_golf_types(self) -> None:
        url = f"{self._GOLF_COMMUNITY_ENDPOINT}/types"
        response: Any = self.get(url).json()

        sec = {}
        for type in json.loads(response.text):
            sec.update({type['name']: type['value']})
        print('GOLF_CLUB = ', sec, '\n')

        url: str = f"{self._GOLF_COMMUNITY_ENDPOINT}/flex-types"
        url: str = f"{self._GOLF_COMMUNITY_ENDPOINT}/flex-types"

        response = self.get(url).json()

        sec: dict = {}
        for type in response:
            sec.update({type['name']: type['id']})
        print('GOLF_FLEX = ', sec, '\n')

    def get_strength_types(self) -> None:
        url: str = "/web-data/exercises/Exercises.json"
        url: str = "/web-data/exercises/Exercises.json"

        sec: Any = self.garth.get("connect", url).json()

        with open(os.path.join(".", "garminworkouts", "models", "strength.py"), "w") as fp:
            json.dump(sec, fp)  # encode dict into JSON

    def get_RHR(self) -> int:
        url: str = f"{self._WELLNESS_SERVICE_ENDPOINT}/wellness/dailyHeartRate"
        url: str = f"{self._WELLNESS_SERVICE_ENDPOINT}/wellness/dailyHeartRate"
        params: dict = {
            "date": date.today(),
        }
        response: Any = self.get(url, params=params).json()['restingHeartRate']

        return int(response)

    def get_hr_zones(self) -> Any:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
        return self.get(url).json()

    def save_hr_zones(self, zones) -> None:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
        self.put(url, json=zones)

    def get_power_zones(self) -> Any:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/sports/all"
        return self.get(url).json()

    def save_power_zones(self, zones) -> None:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/all"
        self.put(url, json=zones)

    def find_events(self):
        url = "race-search/events"

        d1 = datetime.today()
        d2 = d1 + timedelta(days=7)

        params = {
            "eventType": "running",
            "fromDate": d1.strftime('%Y-%m-%d'),
            "toDate": d2.strftime('%Y-%m-%d'),
            "includeInPerson": True,
            "includeVirtual": False,
            "verifiedStatuses": "OFFICIAL,VERIFIED",  # ,NONE
            "includeNst": True,
            "limit": 200,
            "eventsProviders": "garmin-events,gc-discoverable-events,garmin-official-events,ahotu",
            "completionTargetMinValue": 41000,
            "completionTargetMaxValue": 43000,
            "completionTargetDurationType": "distance"
        }

        while True:
            params["fromDate"] = d1.strftime('%Y-%m-%d')
            params["toDate"] = d2.strftime('%Y-%m-%d')
            ev: Response = self.get(url, params=params).json()
            if ev:
                yield ev
                d1 = d2
                d2 = d1 + timedelta(days=7)
            else:
                break

    def get_note(self, note_id) -> Any:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/note/{note_id}"
        return self.get(url).json()

    def save_note(self, note) -> None:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/note"
        return self.post(url, json=note).json()

    def update_note(self, note_id, note) -> None:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/note/{note_id}"
        self.put(url, json=note)

    def delete_note(self, note_id) -> None:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/note/{note_id}"
        self.delete(url)
