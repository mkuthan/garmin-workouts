import re
import os
from typing import Any
from garminworkouts.garmin.garminapi import GarminApi


class GarminTypes(GarminApi):
    _WORKOUT_SERVICE_ENDPOINT = "/workout-service"
    _ACTIVITY_SERVICE_ENDPOINT = "/activity-service"
    _GOLF_COMMUNITY_ENDPOINT = "/gcs-golfcommunity/api/v2/club"

    def updateGarmin(self) -> None:
        file_path = os.path.join(".", "garminworkouts", "garmin", "garminapi.py")
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

    def get_types(self) -> None:
        file_path: str = os.path.join(".", "garminworkouts", "models", "types.py")

        url: str = f"{self._WORKOUT_SERVICE_ENDPOINT}/workout/types"
        response: dict = self.get(url).json()

        self.process_workout_types(file_path, response, 'step')
        self.process_workout_types(file_path, response, 'sport')
        self.process_workout_types(file_path, response, 'condition')
        self.process_workout_types(file_path, response, 'intensity')
        self.process_workout_types(file_path, response, 'target')
        self.process_workout_types(file_path, response, 'equipment')
        self.process_workout_types(file_path, response, 'stroke')
        self.process_workout_types(file_path, response, 'swimInstruction')
        self.process_workout_types(file_path, response, 'drill')

        self.get_activity_types(file_path)
        self.get_event_types(file_path)
        self.get_golf_types(file_path)
        self.get_strength_types()

    def get_activity_types(self, file_path) -> None:
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/activityTypes"
        response: dict = self.get(url).json()

        self.process_activity_types(file_path, response, 'activity')

    def get_event_types(self, file_path) -> None:
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/eventTypes"
        response: dict = self.get(url).json()

        self.process_activity_types(file_path, response, 'event')

    def process_workout_types(self, file_path: str, response: dict, name: str) -> None:
        capitalized_name: str = name[0].upper() + name[1:] if name else ""
        if name == 'target':
            cname = 'workoutTarget'
        else:
            cname: str = name
        dict_str = "\n    "
        for type in response.get(f'workout{capitalized_name}Types', dict):
            dict_str += f"'{str(type.get(f'{cname}TypeKey'))}': {type.get(f'{cname}TypeId')},\n    "

        self.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict=f'{name.upper()}_TYPES')

    def process_activity_types(self, file_path: str, response: dict, name: str) -> None:
        dict_str = "\n    "
        for type in response:
            dict_str += f"'{str(type.get('typeKey'))}': {type.get('typeId')},\n    "

        self.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict=f'{name.upper()}_TYPES')

    def process_golf_types(self, file_path: str, response: dict, name: str) -> None:
        if name == 'club':
            key = 'value'
        else:
            key = 'id'
        dict_str = "\n    "
        for type in response:
            dict_str += f"'{str(type.get('name'))}': {str(type.get(key))},\n    "

        self.update_type_dict(file_path=file_path, dict_str=dict_str, type_dict=f'GOLF_{name.upper()}')

    def get_golf_types(self, file_path) -> None:
        url = f"{self._GOLF_COMMUNITY_ENDPOINT}/types"
        response: dict = self.get(url).json()

        self.process_golf_types(file_path, response, 'club')

        url: str = f"{self._GOLF_COMMUNITY_ENDPOINT}/flex-types"
        response = self.get(url).json()

        self.process_golf_types(file_path, response, 'flex')

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
