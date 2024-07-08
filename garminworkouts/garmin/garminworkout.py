from datetime import date
import logging
import os
from typing import Any, Generator
from requests import Response
from garminworkouts.garmin.garminevent import GarminEvent
from garminworkouts.models.extraction import Extraction
from garminworkouts.models.note import Note
from garminworkouts.models.workout import Workout
from garminworkouts.models.trainingplan import TrainingPlan
from garminworkouts.models.fields import (_ID, _WORKOUT, create_field_name)
import account


class GarminWorkout(GarminEvent):
    def get_workout(self, workout_id) -> Response:
        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        return self.get(url)

    def save_workout(self, workout) -> dict:
        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workout"
        return self.post(url, json=workout).json()

    def update_workout(self, workout_id, workout) -> Response:
        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        return self.put(url, json=workout)

    def delete_workout(self, workout_id) -> Response:
        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        return self.delete(url)

    def schedule_workout(self, workout_id, date) -> dict:
        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data: dict = {"date": date}
        return self.post(url, json=json_data).json()

    def remove_workout(self, workout_id, date) -> Response:
        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        json_data: dict = {"date": date}
        return self.delete(url, json=json_data)

    def download_workout_yaml(self, workout_id, filename) -> dict:
        workout_data: dict = self.get_workout(workout_id).json()
        Extraction.workout_export_yaml(workout_data, filename)
        return workout_data

    def download_workout(self, workout_id, file) -> bytes:
        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workout/FIT/{workout_id}"
        response: bytes = self.download(url)

        with open(file, "wb") as f:
            f.write(response)

        return response

    def workout_export(self, args) -> None:
        for workout in self.list_workouts():
            workout_id: str = Workout.extract_workout_id(workout)
            workout_name: str = Workout.extract_workout_name(workout)
            file: str = os.path.join(args.directory, str(workout_id) + '.fit')
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            self.download_workout(workout_id, file)

    def list_workouts(self, batch_size=100) -> Generator[bytes, Any, None]:
        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workouts"
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

    def workout_list(self) -> None:
        for workout in self.list_workouts():
            Workout.print_workout_summary(workout)

    def external_workouts(self, locale) -> dict:
        url: str = f"web-data/workouts/{locale}/index.json"
        return self.garth.get("connect", url).json().get('workouts')

    def get_external_workout(self, code, locale) -> dict:
        url: str = f"web-data/workouts/{locale}/{code}.json"
        return self.garth.get("connect", url).json()

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
