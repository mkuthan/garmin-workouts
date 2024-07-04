import json
import logging
from datetime import datetime, date, timedelta
from requests import Response
from typing import Any, Literal, Generator, Optional
from garminworkouts.models.event import Event
from garminworkouts.models.fields import (_ID, _WORKOUT, create_field_name)
from garminworkouts.models.note import Note
from garminworkouts.models.trainingplan import TrainingPlan
from garminworkouts.models.workout import Workout
from garminworkouts.models.power import Power
from garminworkouts.models.extraction import Extraction
from garminworkouts.models.settings import settings
import garth
import os
import re
import account


class GarminClient(object):
    _GARMIN_SUBDOMAIN = "connectapi"
    _GARMIN_VERSION = "24.13.2.0"
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

        self.display_name: str = self.garth.profile["userName"]
        self.full_name: str = self.garth.profile["fullName"]
        logging.info("Logged in as %s (%s)", self.full_name, self.display_name)

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
        logging.info("Deleting workout '%s'", workout_id)
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
        date_plus_days: datetime = date + timedelta(days=days)

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

        params: dict = {
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

        logging.info(f"Requesting activities by date from {startdate} to {enddate}")
        while True:
            params["start"] = str(start)
            logging.info(f"Requesting activities {start} to {start+limit}")
            act: Response = self.get(url, params=params).json()
            if act:
                activities.extend(act)
                start: int = start + limit
            else:
                break

        return activities

    def download_activity(self, activity_id) -> bytes:
        url: str = f"{self._DOWNLOAD_SERVICE}/activity/{activity_id}"
        data: bytes = self.download(url)

        newpath: str = os.path.join('.', 'activities')
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        output_file: str = f"./activities/{str(activity_id)}.zip"
        with open(output_file, "wb") as fb:
            fb.write(data)
        return data

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
        file_path: str = os.path.join(".", "garminworkouts", "models", "types.py")

        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workout/types"
        response: dict = self.get(url).json()

        dict_str = "\n    "
        for type in response.get('workoutStepTypes', dict):
            dict_str += f"'{str(type.get('stepTypeKey'))}': {type.get('stepTypeId')},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='STEP_TYPES')

        dict_str = "\n    "
        for type in response.get('workoutSportTypes', dict):
            dict_str += f"'{str(type.get('sportTypeKey'))}': {type.get('sportTypeId')},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='SPORT_TYPES')

        dict_str = "\n    "
        for type in response.get('workoutConditionTypes', dict):
            dict_str += f"'{str(type.get('conditionTypeKey'))}': {type.get('conditionTypeId')},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='END_CONDITIONS')

        dict_str = "\n    "
        for type in response.get('workoutIntensityTypes', dict):
            dict_str += f"'{str(type.get('intensityTypeKey'))}': {type.get('intensityTypeId')},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='INTENSITY_TYPES')

        dict_str = "\n    "
        for type in response.get('workoutTargetTypes', dict):
            dict_str += f"'{str(type.get('workoutTargetTypeKey'))}': {type.get('workoutTargetTypeId')},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='TARGET_TYPES')

        dict_str = "\n    "
        for type in response.get('workoutEquipmentTypes', dict):
            dict_str += f"'{str(type.get('equipmentTypeKey'))}': {type.get('equipmentTypeId')},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='EQUIPMENT_TYPES')

        dict_str = "\n    "
        for type in response.get('workoutStrokeTypes', dict):
            dict_str += f"'{str(type.get('strokeTypeKey'))}': {type.get('strokeTypeId')},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='STROKE_TYPES')

        dict_str = "\n    "
        for type in response.get('workoutSwimInstructionTypes', dict):
            dict_str += f"'{str(type.get('swimInstructionTypeKey'))}': {type.get('swimInstructionTypeId')},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='SWIM_INSTRUCTION_TYPES')

        dict_str = "\n    "
        for type in response.get('workoutDrillTypes', dict):
            dict_str += f"'{str(type.get('drillTypeKey'))}': {type.get('drillTypeId')},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='DRILL_TYPES')

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

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='ACTIVITY_TYPES')

    def get_event_types(self, file_path) -> None:
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/eventTypes"
        response: dict = self.get(url).json()

        dict_str = "\n    "
        for type in response:
            dict_str += f"'{str(type.get('typeKey'))}': {type.get('typeId')},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='EVENT_TYPES')

    def get_golf_types(self, file_path) -> None:
        url = f"{self._GOLF_COMMUNITY_ENDPOINT}/types"
        response: dict = self.get(url).json()

        dict_str = "\n    "
        for type in response:
            dict_str += f"'{str(type.get('name'))}': {str(type.get('value'))},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='GOLF_CLUB')

        url: str = f"{self._GOLF_COMMUNITY_ENDPOINT}/flex-types"
        response = self.get(url).json()

        dict_str = "\n    "
        for type in response:
            dict_str += f"'{str(type.get('name'))}': {str(type.get('id'))},\n    "

        GarminClient.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict='GOLF_FLEX')

    def get_strength_types(self) -> None:
        url: str = "/web-data/exercises/Exercises.json"
        sec: dict = self.garth.get("connect", url).json().get('categories')

        new_dicts: list = []  # List to store the new dictionaries

        for key, value in sec.items():
            # Step 3: For each key-value pair, create a new dictionary
            new_dict: dict = {key: value}

            # Step 5: Store the new dictionary
            new_dicts.append(new_dict)

        with open(os.path.join(".", "garminworkouts", "models", "strength.py"), "w") as fp:
            ind = 0
            for d in new_dicts:
                dict_str: str = ''
                if ind > 0:
                    fp.write("\n")
                s = str(list(d.keys())[0])
                dict_str += s + ' = {\n    '
                q: Any = d.get(s).get('exercises')

                for ex in q:
                    dict_str += '\'' + ex + '\': {\n        '
                    if len('\'primaryMuscles\': ' + repr(q.get(ex).get('primaryMuscles')) + ',') <= 112:
                        dict_str += '\'primaryMuscles\': ' + repr(q.get(ex).get('primaryMuscles')) + ',\n        '
                    else:
                        dict_str += '\'primaryMuscles\': [\n            '
                        comb: str = '\', \''.join(q.get(ex).get('primaryMuscles')) + ',\n'
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

    def find_events(self) -> Generator[Response, dict, None]:
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

    def activity_list(self) -> None:
        try:
            start_date: date = date.today() - timedelta(days=7)
            end_date: date = date.today()
            activities: list[dict] = self.get_activities_by_date(
                startdate=start_date, enddate=end_date, activitytype='running')
            for activity in activities:
                id: str = activity.get('activityId', '')
                logging.info("Downloading activity '%s'", id)
                self.download_activity(id)
        except Exception as e:
            logging.error("An error occurred: %s", str(e))

    def trainingplan_reset(self, args) -> None:
        workouts, notes, plan = settings(args)
        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in self.list_workouts()}
        for workout in workouts:
            workout_name: str = workout.get_workout_name()
            existing_workout: dict | None = existing_workouts_by_name.get(workout_name)
            if existing_workout and plan in existing_workout.get('description'):
                workout_id: str = Workout.extract_workout_id(existing_workout)
                try:
                    logging.info("Deleting workout '%s'", workout_name)
                    self.delete_workout(workout_id)
                except Exception as e:
                    logging.error("Error deleting workout '%s': %s", workout_name, str(e))

    def updateGarmin(self) -> None:
        file_path = "./garminworkouts/garmin/garminclient.py"
        flags = 0
        subs: str = self.version

        with open(file_path, "r+") as file:
            file_contents: str = file.read()
            text: str = re.findall('_GARMIN_VERSION = "(.*)\"', file_contents)[0]
            text_pattern: re.Pattern[str] = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(subs, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)

        self.get_types()

    def _find_events(self) -> None:
        events = self.find_events()
        for subev in events:
            for ev in subev:
                ev_a = json.loads(ev.decode('utf-8'))
                if ('administrativeArea' in ev_a) and (ev_a.get('administrativeArea') is not None) and (
                     ev_a.get('administrativeArea', {}).get('countryCode') is not None):
                    newpath: str = os.path.join('.', 'exported', 'events', ev_a.get('eventType'),
                                                ev_a.get('administrativeArea', {}).get('countryCode'))
                else:
                    newpath: str = os.path.join('.', 'exported', 'events', ev_a.get('eventType'))
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                file: str = os.path.join(newpath, ev_a.get('eventRef') + '.yaml')
                Extraction.event_export_yaml(event=self.get(ev_a.get('detailsEndpoints')[0].get('url')
                                                            ).json(), filename=file)

    def workout_export(self, args) -> None:
        for workout in self.list_workouts():
            workout_id: str = Workout.extract_workout_id(workout)
            workout_name: str = Workout.extract_workout_name(workout)
            file: str = os.path.join(args.directory, str(workout_id) + '.fit')
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            self.download_workout(workout_id, file)

    def user_zones(self) -> None:
        _, _, data = Workout(
            [],
            [],
            account.vV02,
            account.fmin,
            account.fmax,
            account.flt,
            account.rFTP,
            account.cFTP,
            str(''),
            date.today()).hr_zones()

        _, _, _, pdata = Power.power_zones(account.rFTP, account.cFTP)

        self.save_hr_zones(data)
        self.save_power_zones(pdata)

        Workout([],
                [],
                account.vV02,
                account.fmin,
                account.fmax,
                account.flt,
                account.rFTP,
                account.cFTP,
                str(''),
                date.today()
                ).zones()

    def workout_export_yaml(self) -> None:
        for workout in self.external_workouts(account.locale):
            code: str = workout.get('workoutSourceId', '')
            sport: str = workout.get('sportTypeKey', '')
            difficulty: str = workout.get('difficulty', '')
            workout: dict = self.get_external_workout(code, account.locale)
            workout[create_field_name(_WORKOUT, _ID)] = code

            workout_id: str = Workout.extract_workout_id(workout)
            workout_name: str = Workout.extract_workout_name(workout)
            newpath: str = os.path.join('.', 'workouts', sport, difficulty)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            file: str = os.path.join(newpath, str(workout_id) + '.yaml')
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            Extraction.workout_export_yaml(workout, file)

        for tp in self.list_trainingplans(account.locale):
            tp: dict = TrainingPlan.export_trainingplan(tp)
            tp_type: str = tp.get('type', '')
            tp_subtype: str = tp.get('subtype', '')
            tp_level: str = tp.get('level', '')
            tp_version: str = tp.get('version', '')
            tp_name: str = ''.join(letter for letter in tp.get('name', '') if letter.isalnum())

            tp = self.schedule_training_plan(tp.get(_ID), str(date.today()))

            if tp_subtype == 'RunningOther':
                tp_subtype = tp_name
                tp_name = ''

            if (tp_subtype.lower() == tp_name.lower()) or ((tp_subtype + tp_type).lower() == tp_name.lower()):
                newpath: str = os.path.join('.', 'trainingplans', tp_type, 'Garmin', tp_subtype, tp_level, tp_version)
            else:
                newpath: str = os.path.join('.', 'trainingplans', tp_type, 'Garmin', tp_subtype, tp_level, tp_version,
                                            tp_name)

            for w in self.get_training_plan(TrainingPlan.export_trainingplan(tp).get(_ID), account.locale):
                week: str = w.get('weekId')
                day: str = w.get('dayOfWeekId')
                name: str = f'R{week}_{day}'

                if not os.path.exists(newpath):
                    os.makedirs(newpath)

                file: str = os.path.join(newpath, name + '.yaml')

                if w.get('taskWorkout'):
                    workout_id: str = w.get('taskWorkout', {}).get('workoutId')
                    workout_data: Response = self.get_workout(workout_id)
                    workout = workout_data.json()
                    logging.info("Exporting workout '%s' into '%s'", name, file)
                    Extraction.workout_export_yaml(workout, file)
                if w.get('taskNote'):
                    config: dict = {}
                    config['name'] = w.get('taskNote', {}).get('note')
                    config['content'] = w.get('taskNote', {}).get('noteDescription')
                    note = Note(config)
                    logging.info("Exporting note '%s' into '%s'", name, file)
                    Extraction.note_export_yaml(note, file)

            self.delete_training_plan(tp.get('trainingPlanId'))

    def workout_list(self) -> None:
        for workout in self.list_workouts():
            Workout.print_workout_summary(workout)

    def event_list(self) -> None:
        for event in self.list_events():
            Event.print_event_summary(event)

    def trainingplan_list(self) -> None:
        for tp in self.list_trainingplans(account.locale):
            TrainingPlan.print_trainingplan_summary(tp)

    def update_workouts(self, ue, workouts: list[Workout], plan: str) -> None:
        workouts_by_name: dict[str, Workout] = {w.get_workout_name(): w for w in workouts}

        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in self.list_workouts()}
        c: int = 0

        for wname in ue:
            existing_workout: dict | None = existing_workouts_by_name.get(wname)
            description: dict | None = existing_workout.get('description') if existing_workout else None
            if description and plan in description:
                workout_id: str = Workout.extract_workout_id(existing_workout)
                workout_owner_id: str = Workout.extract_workout_owner_id(existing_workout)
                workout_author: dict = Workout.extract_workout_author(existing_workout)
                workout: Workout = workouts_by_name[wname]
                payload: dict = workout.create_workout(workout_id, workout_owner_id, workout_author)
                logging.info("Updating workout '%s'", wname)
                self.update_workout(workout_id, payload)
                c += 1

        for workout in workouts:
            day_d, *_ = workout.get_workout_date()
            if date.today() <= day_d < date.today() + timedelta(weeks=2):
                workout_name: str = workout.get_workout_name()
                existing_workout = existing_workouts_by_name.get(workout_name)
                if not existing_workout:
                    payload = workout.create_workout()
                    logging.info("Creating workout '%s'", workout_name)
                    workout_id = Workout.extract_workout_id(self.save_workout(payload))
                    self.schedule_workout(workout_id, day_d.isoformat())
                    c += 1
        if c == 0:
            logging.info('No workouts to update')

    def update_notes(self, ne, notes: list[Note], plan: str) -> None:
        for note in notes:
            day_d, _, _ = note.get_note_date()
            if date.today() <= day_d < date.today() + timedelta(weeks=2):
                note_name: str = note.get_note_name()
                existing_note: dict | None = ne.get(note_name)
                if not existing_note:
                    payload: dict = note.create_note(date=day_d.isoformat())
                    logging.info("Creating note '%s'", note_name)
                    self.save_note(note=payload)
                else:
                    note_id: str | None = existing_note.get('noteId')
                    note_obj: Note = ne.get(note_name)
                    payload = note_obj.create_note(note_id)
                    logging.info("Updating note '%s'", note_name)
                    if existing_note.get('trainingPlanId'):
                        self.update_note(note_id=note_id, note=payload)
                        self.save_note(note=payload)
                    else:
                        self.update_note(note_id=note_id, note=payload)
                        self.save_note(note=payload)

    def update_events(self, events) -> None:
        c: int = 0
        existing_events_by_name: dict = {Event.extract_event_name(w): w for w in self.list_events()}
        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in self.list_workouts()}

        for event in events:
            if event.date >= date.today():
                existing_event: dict | None = existing_events_by_name.get(event.name)
                existing_workout: dict | None = existing_workouts_by_name.get(event.name)
                workout_id: str | None = Workout.extract_workout_id(existing_workout) if existing_workout else None

                if existing_event:
                    if event.date < date.today() + timedelta(weeks=1):
                        event_id: str = Event.extract_event_id(existing_event)
                        payload: dict = event.create_event(event_id, workout_id)
                        logging.info("Updating event '%s'", event.name)
                        self.update_event(event_id, payload)
                        c += 1
                else:
                    payload = event.create_event(workout_id=workout_id)
                    logging.info("Creating event '%s'", event.name)
                    self.save_event(payload)
                    c += 1
        if c == 0:
            logging.info('No events to update')

    @staticmethod
    def update_type_dict(file_path: str, dict_str: str, type_dict: str) -> None:
        """
        Updates the dictionary string for a given club name in a file.

        Parameters:
        - file_path: The path to the file to be updated.
        - dict_str: The new dictionary string to replace the old one.
        - type_dict: The name of the club whose dictionary is to be updated.
        """
        flags = 0
        pattern_str: str = f'{type_dict}: dict\\[str, int\\] = \\{{([^}}]*)\\}}'
        with open(file_path, "r+") as file:
            file_contents: str = file.read()
            text: str = re.findall(pattern_str, file_contents)[0]
            text_pattern: re.Pattern[str] = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(dict_str, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)
