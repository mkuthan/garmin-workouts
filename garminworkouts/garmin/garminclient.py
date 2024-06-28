import logging
from datetime import datetime, date, timedelta
from requests import Response
from typing import Any, Literal, Generator, Optional
from garminworkouts.models.extraction import Extraction
import garth
import os
import re


class GarminClient(object):
    _GARMIN_SUBDOMAIN = "connectapi"
    _GARMIN_VERSION = "24.13.1.0"
    _WORKOUT_SERVICE_ENDPOINT = "/workout-service"
    _CALENDAR_SERVICE_ENDPOINT = "/calendar-service"
    _ACTIVITY_SERVICE_ENDPOINT = "/activity-service"
    _BIOMETRIC_SERVICE_ENDPOINT = "/biometric-service"
    _WELLNESS_SERVICE_ENDPOINT = "/wellness-service"
    _ACTIVITY_LIST_SERVICE_ENDPOINT = "/activitylist-service"
    _TRAINING_PLAN_SERVICE_ENDPOINT = "/trainingplan-service/trainingplan"
    _GOLF_COMMUNITY_ENDPOINT = "/gcs-golfcommunity/api/v2/club"
    _BADGE_CHALLENGE_ENDPOINT = "/badgechallenge-service"
    _DOWNLOAD_SERVICE = "/download-service/files"

    def __init__(self, email, password) -> None:
        self.email: str = email
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
            self.garth.login(self.email, self.password, prompt_mfa=self.get_mfa)
            # Save tokens for next login
            self.garth.dump("./garminconnect")

        self.display_name: str = self.garth.profile["displayName"]
        self.full_name: str = self.garth.profile["fullName"]

        settings: dict = self.get("/userprofile-service/userprofile/user-settings").json()
        self.unit_system: dict | None = settings["userData"]["measurementSystem"] if settings is not None else None

        try:
            self.version: str = self.get("/info-service/api/system/release-system").json()[0].get('version', '')
        except IndexError:
            self.version = GarminClient._GARMIN_VERSION
        try:
            assert self.version == GarminClient._GARMIN_VERSION
        except AssertionError:
            logging.error('Updated version: ' + self.version + ' from ' + GarminClient._GARMIN_VERSION)

        return True

    def get_mfa(self) -> str:
        """Get MFA."""

        return input("MFA one-time code: ")

    def get(self, *args, **kwargs) -> Response:
        return self.garth.get(GarminClient._GARMIN_SUBDOMAIN, *args, **kwargs)

    def put(self, *args, **kwargs) -> Response:
        return self.garth.put(GarminClient._GARMIN_SUBDOMAIN, *args, **kwargs)

    def post(self, *args, **kwargs) -> Response:
        return self.garth.post(GarminClient._GARMIN_SUBDOMAIN, *args, **kwargs)

    def delete(self, *args, **kwargs) -> Response:
        return self.garth.delete(GarminClient._GARMIN_SUBDOMAIN, *args, **kwargs)

    def download(self, path, **kwargs) -> bytes:
        return self.garth.download(path, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None

    def external_workouts(self, locale) -> dict:
        url: str = f"web-data/workouts/{locale}/index.json"
        return self.garth.get("connect", url).json().get('workouts')

    def get_external_workout(self, code, locale) -> dict:
        url: str = f"web-data/workouts/{locale}/{code}.json"
        return self.garth.get("connect", url).json()

    def list_workouts(self, batch_size=100) -> Generator[bytes, Any, None]:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workouts"
        start_index = 0

        while True:
            params: dict = {
                "start": start_index,
                "limit": batch_size,
                "myWorkoutsOnly": False,
                "sharedWorkoutsOnly": False,
                "orderBy": "WORKOUT_NAME",
                "orderSeq": "ASC",
                "includeAtp": True
            }
            response_jsons: dict = self._fetch_workouts(url, params).json()
            if not response_jsons:
                break
            for response_json in response_jsons:
                yield response_json

            start_index += batch_size

    def _fetch_workouts(self, url: str, params: dict) -> Response:
        response: Response = self.get(url, params=params)
        return response

    def get_workout(self, workout_id) -> Response:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        return self.get(url)

    def download_workout_yaml(self, workout_id, filename) -> dict:
        workout_data: dict = self.get_workout(workout_id).json()
        Extraction.workout_export_yaml(workout_data, filename)
        return workout_data

    def download_note_yaml(self, trainingplan, note_id, filename) -> dict:
        note_data: dict = self.get_note(trainingplan, note_id).json()
        Extraction.note_export_yaml(note_data, filename)
        return note_data

    def download_workout(self, workout_id, file) -> bytes:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/FIT/{workout_id}"
        response: bytes = self.download(url)

        with open(file, "wb") as f:
            f.write(response)

        return response

    def save_workout(self, workout) -> dict:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout"
        return self.post(url, json=workout).json()

    def update_workout(self, workout_id, workout) -> Response:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        return self.put(url, json=workout)

    def delete_workout(self, workout_id) -> Response:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        return self.delete(url)

    def get_calendar(self, date, days=7) -> tuple[list[str], list[str], dict]:
        year = str(date.year)
        month = str(date.month - 1)
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}"
        response_jsons: dict = self.get(url).json().get('calendarItems')
        updateable_elements: list[str] = []
        checkable_elements: list[str] = []
        note_elements: dict = {}
        date_plus_days = date + timedelta(days=days)

        for item in response_jsons:
            item_date = datetime.strptime(item.get('date'), '%Y-%m-%d').date()
            item_type: Any = item.get('itemType')

            if item_type == 'workout':
                if item_date < date:
                    logging.info("Deleting workout '%s'", item.get('title'))
                    self.delete_workout(item.get('workoutId'))
                elif item_date < date_plus_days:
                    updateable_elements.append(item.get('title'))

            elif item_type == 'activity':
                payload: dict = self.get_activity_workout(item.get('id'))
                if 'workoutName' in payload:
                    checkable_elements.append(payload.get('workoutName', str))

            elif item_type == 'note':
                if item.get('trainingPlanId'):
                    payload = self.get_note(trainingplan=True, note_id=item.get('id')).json()
                else:
                    payload = self.get_note(trainingplan=False, note_id=item.get('id')).json()
                note_elements[payload.get('noteName')] = payload

        return updateable_elements, checkable_elements, note_elements

    def schedule_workout(self, workout_id, date) -> dict:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data: dict = {"date": date}
        return self.post(url, json=json_data).json()

    def remove_workout(self, workout_id, date) -> Response:
        url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data: dict = {"date": date}
        return self.delete(url, json=json_data)

    def list_events(self, batch_size=20) -> Generator[dict, dict, None]:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/events"
        start_index = 1
        all_events_fetched = False
        while not all_events_fetched:
            params: dict = {
                "startDate": datetime.today(),
                "pageIndex": start_index,
                "limit": batch_size
            }
            response: dict = self.get(url, params=params).json()
            if not response or response == []:
                all_events_fetched = True
            else:
                for response_json in response:
                    yield response_json
            start_index += batch_size

    def get_event(self, event_id) -> dict:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"
        return self.get(url).json()

    def save_event(self, event) -> dict:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event"
        return self.post(url, json=event).json()

    def update_event(self, event_id, event) -> Response:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"
        return self.put(url, json=event)

    def delete_event(self, event_id) -> Response:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"
        return self.delete(url)

    def get_activity(self, activity_id) -> dict:
        url: str = f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/{activity_id}"
        return self.get(url).json()

    def get_activity_workout(self, activity_id) -> Any:
        url: str = f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/{activity_id}/workouts"
        a: dict = self.get(url).json()
        return [] if len(a) == 0 else a[0]

    def get_activities_by_date(self,
                               startdate=None, enddate=None,
                               activitytype=None,
                               minDistance=None, maxDistance=None,  # meters
                               minDuration=None, maxDuration=None,  # seconds
                               minElevation=None, maxElevation=None,  # meters
                               ) -> list[dict]:
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

    def download_activity(self, activity_id) -> None:
        url: str = f"{self._DOWNLOAD_SERVICE}/activity/{activity_id}"
        data: bytes = self.download(url)

        newpath: str = os.path.join('.', 'activities')
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        output_file: str = f"./activities/{str(activity_id)}.zip"
        with open(output_file, "wb") as fb:
            fb.write(data)

    def list_trainingplans(self, locale) -> dict:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/search"
        params: dict = {
            "start": '1',
            "limit": '1000',
            "locale": locale.split('-')[0],
        }
        headers: dict = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        return self.post(url, params=params, api=True, headers=headers).json().get('trainingPlanList')

    def schedule_training_plan(self, plan_id, startDate) -> dict:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/schedule/{plan_id}"
        params: dict = {
            "startDate": startDate,
        }
        return self.get(url, params=params).json()

    def get_training_plan(self, plan_id, locale) -> dict:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/tasks/{plan_id}"
        params: dict = {
            "localeKey": locale,
        }
        return self.get(url, params=params).json()

    def delete_training_plan(self, plan_id) -> Response:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/trainingplan/{plan_id}"
        return self.delete(url)

    def get_types(self) -> None:
        file_path = os.path.join(".", "garminworkouts", "models", "types.py")

        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workout/types"
        response: dict = self.get(url).json()

        flags = 0

        dict_str = "\n    "
        for type in response.get('workoutStepTypes', dict):
            dict_str += f"'{str(type.get('stepTypeKey'))}': {type.get('stepTypeId')},\n    "

        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'STEP_TYPES: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        dict_str = "\n    "
        for type in response.get('workoutSportTypes', dict):
            dict_str += f"'{str(type.get('sportTypeKey'))}': {type.get('sportTypeId')},\n    "

        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'SPORT_TYPES: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        dict_str = "\n    "
        for type in response.get('workoutConditionTypes', dict):
            dict_str += f"'{str(type.get('conditionTypeKey'))}': {type.get('conditionTypeId')},\n    "

        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'END_CONDITIONS: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        dict_str = "\n    "
        for type in response.get('workoutIntensityTypes', dict):
            dict_str += f"'{str(type.get('intensityTypeKey'))}': {type.get('intensityTypeId')},\n    "

        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'INTENSITY_TYPES: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        dict_str = "\n    "
        for type in response.get('workoutTargetTypes', dict):
            dict_str += f"'{str(type.get('workoutTargetTypeKey'))}': {type.get('workoutTargetTypeId')},\n    "

        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'TARGET_TYPES: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        dict_str = "\n    "
        for type in response.get('workoutEquipmentTypes', dict):
            dict_str += f"'{str(type.get('equipmentTypeKey'))}': {type.get('equipmentTypeId')},\n    "

        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'EQUIPMENT_TYPES: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        dict_str = "\n    "
        for type in response.get('workoutStrokeTypes', dict):
            dict_str += f"'{str(type.get('strokeTypeKey'))}': {type.get('strokeTypeId')},\n    "

        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'STROKE_TYPES: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        dict_str = "\n    "
        for type in response.get('workoutSwimInstructionTypes', dict):
            dict_str += f"'{str(type.get('swimInstructionTypeKey'))}': {type.get('swimInstructionTypeId')},\n    "

        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'SWIM_INSTRUCTION_TYPES: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        dict_str = "\n    "
        for type in response.get('workoutDrillTypes', dict):
            dict_str += f"'{str(type.get('drillTypeKey'))}': {type.get('drillTypeId')},\n    "

        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'DRILL_TYPES: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        self.get_activity_types(file_path)
        self.get_event_types(file_path)
        self.get_golf_types(file_path)
        self.get_strength_types()

    def get_activity_types(self, file_path) -> None:
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/activityTypes"
        response: dict = self.get(url).json()

        dict_str = "\n    "
        for type in response:
            dict_str += f"'{str(type.get('typeKey'))}': {type.get('typeId')},\n    "

        flags = 0
        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'ACTIVITY_TYPES: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

    def get_event_types(self, file_path) -> None:
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/eventTypes"
        response: dict = self.get(url).json()

        dict_str = "\n    "
        for type in response:
            dict_str += f"'{str(type.get('typeKey'))}': {type.get('typeId')},\n    "

        flags = 0
        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'EVENT_TYPES: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

    def get_golf_types(self, file_path) -> None:
        url = f"{self._GOLF_COMMUNITY_ENDPOINT}/types"
        response: dict = self.get(url).json()

        dict_str = "\n    "
        for type in response:
            dict_str += f"'{str(type.get('name'))}': {str(type.get('value'))},\n    "

        flags = 0
        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'GOLF_CLUB: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        url: str = f"{self._GOLF_COMMUNITY_ENDPOINT}/flex-types"
        response = self.get(url).json()

        dict_str = "\n    "
        for type in response:
            dict_str += f"'{str(type.get('name'))}': {str(type.get('id'))},\n    "

        with open(file_path, "r+") as file:
            file_contents = file.read()
            text: str = re.findall(r'GOLF_FLEX: dict\[str, int\] = \{([^}]*)\}', file_contents)[0]
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

    def get_strength_types(self) -> None:
        url: str = "/web-data/exercises/Exercises.json"
        sec: dict = self.garth.get("connect", url).json().get('categories')

        new_dicts = []  # List to store the new dictionaries

        for key, value in sec.items():
            # Step 3: For each key-value pair, create a new dictionary
            new_dict = {key: value}

            # Step 5: Store the new dictionary
            new_dicts.append(new_dict)

        with open(os.path.join(".", "garminworkouts", "models", "strength.py"), "w") as fp:
            ind = 0
            for d in new_dicts:
                dict_str = ''
                if ind > 0:
                    fp.write("\n")
                s = str(list(d.keys())[0])
                dict_str += s + ' = {\n    '
                q = d.get(s).get('exercises')

                for ex in q:
                    dict_str += '\'' + ex + '\': {\n        '
                    if len('\'primaryMuscles\': ' + repr(q.get(ex).get('primaryMuscles')) + ',') <= 112:
                        dict_str += '\'primaryMuscles\': ' + repr(q.get(ex).get('primaryMuscles')) + ',\n        '
                    else:
                        dict_str += '\'primaryMuscles\': [\n            '
                        comb = '\', \''.join(q.get(ex).get('primaryMuscles')) + ',\n'
                        dict_str += "\'" + comb[:-2] + "\'\n"
                        dict_str += '        ],\n        '
                    if len('\'secondaryMuscles\': ' + repr(q.get(ex).get('secondaryMuscles')) + ',\n    ') <= 112:
                        dict_str += '\'secondaryMuscles\': ' + repr(q.get(ex).get('secondaryMuscles')) + ',\n    '
                    else:
                        dict_str += '\'secondaryMuscles\': [\n            '
                        comb = '\', \''.join(q.get(ex).get('secondaryMuscles')) + ',\n'
                        dict_str += "\'" + comb[:-2] + "\'\n"
                        dict_str += '        ],\n    '
                    dict_str += '},\n    '

                fp.write(dict_str + "}\n")
                ind += 1

    def get_RHR(self) -> int:
        url: str = f"{self._WELLNESS_SERVICE_ENDPOINT}/wellness/dailyHeartRate"
        params: dict = {
            "date": date.today(),
        }
        response: str = self.get(url, params=params).json().get('restingHeartRate', '')

        return int(response)

    def get_hr_zones(self) -> dict:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
        return self.get(url).json()

    def save_hr_zones(self, zones) -> Response:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
        return self.put(url, json=zones)

    def get_power_zones(self) -> dict:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/sports/all"
        return self.get(url).json()

    def save_power_zones(self, zones) -> Response:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/all"
        return self.put(url, json=zones)

    def find_events(self) -> Generator[Response, Any, None]:
        url = "race-search/events"

        d1 = datetime.today()
        d2 = d1 + timedelta(days=7)

        params: dict = {
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
            params['fromDate'] = d1.strftime('%Y-%m-%d')
            params['toDate'] = d2.strftime('%Y-%m-%d')
            ev: Response = self.get(url, params=params).json()
            if ev:
                yield ev
                d1: datetime = d2
                d2: datetime = d1 + timedelta(days=7)
            else:
                break

    def get_note(self, trainingplan, note_id) -> Response:
        if trainingplan:
            url: str = f"{GarminClient._TRAINING_PLAN_SERVICE_ENDPOINT}/scheduled/notes/{note_id}"
        else:
            url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/note/{note_id}"
        return self.get(url)

    def save_note(self, note) -> dict:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/note"
        return self.post(url, json=note).json()

    def update_note(self, note_id, note) -> Response:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/note/{note_id}"
        return self.put(url, json=note)

    def delete_note(self, note_id) -> Response:
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/note/{note_id}"
        return self.delete(url)

    def list_challenge(self) -> None:
        url: str = f"{GarminClient._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/available"
        challenges: dict = self.get(url).json()
        for challenge in challenges:
            url: str = (
                f"{GarminClient._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/"
                f"{challenge.get('uuid')}/optIn/"
                f"{datetime.today().strftime('%Y-%m-%d')}"
                )

            self.post(url)
