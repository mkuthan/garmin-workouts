import json
import datetime

from garminworkouts.models.duration import Duration
from garminworkouts.models.power import Power
from datetime import date, timedelta
from garminworkouts.utils import functional, math
import yaml

SPORT_TYPES = {
    "running": 1,
    "cycling": 2,
    "swimming": 4,
    "strength_training": 5,
    "cardio_training": 6,
    "yoga": 7,
    "hiit": 9,
    "other": 9
}

STEP_TYPES = {
    "warmup": 1,
    "cooldown": 2,
    "run": 3,
    "interval": 3,
    "recovery": 4,
    "rest": 5,
    "repeat": 6,
    "other": 7
}

END_CONDITIONS = {
    "lap.button": 1,
    "time": 2,
    "distance": 3,
    "calories": 4,
    "power": 5,         # Potencia por encima de un umbral ("endConditionCompare": "gt")
                        # Potencia por debajo de un umbral ("endConditionCompare": "lt")
    "heart.rate": 6,    # Pulsaciones por encima de un umbral ("endConditionCompare": "lt")
                        # Pulsaciones por debajo de un umbral ("endConditionCompare": "gt")
}

TARGET_TYPES = {
    "no.target": 1,
    "power.zone": 2,
    "cadence.zone": 3,
    "cadence": 3,
    "heart.rate.zone": 4,
    "speed.zone": 5,
    "pace.zone": 6,  # meters per second
    "power.curve": 16
}

STROKE_TYPES = {
    "any_stroke": 1,        # Cualquiera
    "backstroke": 2,        # Espalda
    "breaststroke": 3,      # Braza
    "drill": 4,             # Tecnica
    "fly": 5,               # Mariposa
    "free": 6,              # Croll
    "individual_medley": 7  # Estilos
}

EQUIPMENT_TYPES = {
    "fins": 1,          # Aletas
    "kickboard": 2,     # Tabla
    "paddles": 3,       # Palas
    "pull_buoy": 4,     # Pull buoy
    "snorkel": 5,       # Tubo buceo
    "none": 0           # Sin equipo
}

POOL_LENGTHS = {
    "short": 25,
    "olympic": 50
}


@staticmethod
def step_extraction(step_json):
    if step_json['stepType']['stepTypeKey'] != 'repeat':
        step = {}
        step['type'] = step_json['stepType']['stepTypeKey']

        if step_json['endCondition']['conditionTypeKey'] == 'time':
            step['duration'] = str(timedelta(seconds=int(step_json['endConditionValue'])))
        elif step_json['endCondition']['conditionTypeKey'] == 'distance':
            step['duration'] = str(float(step_json['endConditionValue'])/1000) + 'km'

        step['target'] = {}
        step['target']['type'] = step_json['targetType']['workoutTargetTypeKey']
        if step['target']['type'] == 'pace.zone':
            step['target']['min'] = str(timedelta(seconds=int(1000 / float(step_json['targetValueOne']))))[2:]
            step['target']['max'] = str(timedelta(seconds=int(1000 / float(step_json['targetValueTwo']))))[2:]
        elif step['target']['type'] == 'cadence':
            step['target']['min'] = str(int(step_json['targetValueOne']))
            step['target']['max'] = str(int(step_json['targetValueTwo']))

        step['description'] = step_json['description'] if step_json['description'] else ''

        return step


class Workout(object):
    _WORKOUT_ID_FIELD = "workoutId"
    _WORKOUT_NAME_FIELD = "workoutName"
    _WORKOUT_DESCRIPTION_FIELD = "description"
    _WORKOUT_OWNER_ID_FIELD = "ownerId"
    _WORKOUT_SPORT_TYPE_FIELD = "sportType"
    _WORKOUT_SEGMENTS_FIELD = "workoutSegments"
    _WORKOUT_STEPS_FIELD = "workoutSteps"
    _WORKOUT_ORDER_FIELD = "segmentOrder"

    def __init__(
            self,
            config=[],
            target=[],
            vVO2=Duration('5:00'),
            fmin=60,
            fmax=200,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan=[],
            race=date(1, 1, 1)
            ):

        self.sport_type = config['sport'].lower() if 'sport' in config else None,
        self.config = config
        self.date = config['date'] if 'date' in config else None
        self.target = target
        self.vVO2 = vVO2.to_seconds()
        self.fmin = fmin
        self.fmax = fmax
        self.rFTP = rFTP.to_watts(0, 0)
        self.cFTP = cFTP.to_watts(0, 0)
        self.plan = plan
        self.race = race

        self.duration = datetime.timedelta(seconds=0)
        self.mileage = 0
        self.tss = 0
        self.ratio = 0
        self.norm_pwr = 0
        self.int_fct = 0

        flatten_steps = functional.flatten(self.config["steps"]) if 'steps' in self.config else []

        if self.sport_type[0] == "running":
            self.running_values(flatten_steps)
        elif self.sport_type[0] == "cycling":
            self.cycling_values(flatten_steps)

    def running_values(self, flatten_steps):
        sec = 0
        meters = 0
        duration_secs = 0
        duration_meters = 0

        for step in flatten_steps:
            if not self._end_condition(step)['conditionTypeKey'] == 'lap.button':
                if self._end_condition(step)['conditionTypeKey'] == 'time':
                    duration_secs = self._end_condition_value(step)
                    duration_meters = round(duration_secs * self._equivalent_pace(step))
                if self._end_condition(step)['conditionTypeKey'] == 'distance':
                    duration_meters = self._end_condition_value(step)
                    duration_secs = round(duration_meters / self._equivalent_pace(step))

                sec = sec + duration_secs
                meters = meters + duration_meters

        try:
            self.ratio = round(self.vVO2 / (sec / meters * 1000) * 100)
        except ValueError:
            self.ratio = 0

        self.duration = datetime.timedelta(seconds=sec)
        self.mileage = round(meters/1000, 2)
        self.tss = round(sec/3600 * (self.ratio * 0.89) ** 2 / 100)

    def cycling_values(self, flatten_steps):
        seconds = 0
        xs = []

        for step in flatten_steps:
            power = self._get_power(step)
            power_watts = power.to_watts(self.cFTP) if power else None
            duration = self._get_duration(step)
            duration_secs = duration.to_seconds() if duration else None

            if power_watts and duration_secs:
                seconds = seconds + duration_secs
                xs = functional.concatenate(xs, functional.fill(power_watts, duration_secs))

        self.norm_pwr = math.normalized_power(xs)
        self.int_fct = math.intensity_factor(self.norm_pwr, self.cFTP)
        self.tss = math.training_stress_score(seconds, self.norm_pwr, self.cFTP)

    def zones(self):
        zones = [0.46, 0.6, 0.7, 0.8, 0.84, 1.0, 1.1]
        hr_zones = [round(self.fmin + (self.fmax - self.fmin) * zone) for zone in zones]
        print('::Heart Rate Zones::')
        for i in range(len(zones)-1):
            print('Zone ', i, ': ', hr_zones[i], '-', hr_zones[i + 1])

        zones = [0.6, 0.8, 0.88, 0.95, 1.05, 1.15, 1.28, 1.45]
        power_zones = [round(self.rFTP * zone) for zone in zones]
        print('::Running Power Zones::')
        for i in range(len(zones)-1):
            print('Zone ', i, ': ', power_zones[i], '-', power_zones[i + 1])

    def create_workout(self, workout_id=None, workout_owner_id=None):
        return {
            self._WORKOUT_ID_FIELD: workout_id,
            self._WORKOUT_OWNER_ID_FIELD: workout_owner_id,
            self._WORKOUT_NAME_FIELD: self.get_workout_name(),
            self._WORKOUT_DESCRIPTION_FIELD: self._generate_description(),
            self._WORKOUT_SPORT_TYPE_FIELD: self.get_sport_type(self.sport_type[0]),
            self._WORKOUT_SEGMENTS_FIELD: [
                {
                    self._WORKOUT_ORDER_FIELD: 1,
                    self._WORKOUT_SPORT_TYPE_FIELD: self.get_sport_type(self.sport_type[0]),
                    self._WORKOUT_STEPS_FIELD: self._steps(self.config["steps"])
                }
            ]
        }

    def get_workout_name(self):
        return self.config["name"] + '-' + self.config["description"]

    def get_workout_date(self):
        return date(self.date['year'], self.date['month'], self.date['day'])  # type: ignore

    @staticmethod
    def extract_workout_id(workout):
        return workout[Workout._WORKOUT_ID_FIELD]

    @staticmethod
    def extract_workout_name(workout):
        return workout[Workout._WORKOUT_NAME_FIELD]

    @staticmethod
    def extract_workout_description(workout):
        return workout[Workout._WORKOUT_DESCRIPTION_FIELD]

    @staticmethod
    def extract_workout_owner_id(workout):
        return workout[Workout._WORKOUT_OWNER_ID_FIELD]

    @staticmethod
    def print_workout_json(workout):
        print(json.dumps(functional.filter_empty(workout)))

    @staticmethod
    def print_workout_summary(workout):
        workout_id = Workout.extract_workout_id(workout)
        workout_name = Workout.extract_workout_name(workout)
        workout_description = Workout.extract_workout_description(workout)
        print("{0} {1:20} {2}".format(workout_id, workout_name, workout_description))

    @staticmethod
    def _get_duration(step_config):
        duration = step_config.get("duration")
        return Duration(str(duration)) if duration else None

    @staticmethod
    def _get_power(step):
        power = step.get("power")
        return Power(str(power)) if power else None

    def get_sport_type(self, sport_type):
        return {
                "sportTypeId": SPORT_TYPES[sport_type],
                "sportTypeKey": sport_type,
            }

    def get_step_type(self, step_type):
        return {
                "stepTypeId": STEP_TYPES[step_type],
                "stepTypeKey": step_type,
            }

    def get_end_condition(self, end_condition):
        return {
                "conditionTypeId": END_CONDITIONS[end_condition],
                "conditionTypeKey": end_condition,
            }

    def get_target_type(self, target_type):
        return {
                "workoutTargetTypeId": TARGET_TYPES[target_type],
                "workoutTargetTypeKey": target_type,
            }

    def get_stroke_type(self, stroke_type):
        return {
                "strokeTypeId": STROKE_TYPES[stroke_type],
                "strokeTypeKey": stroke_type,
            }

    def get_equipment_type(self, equipment_type):
        return {
                "equipmentTypeId": EQUIPMENT_TYPES[equipment_type],
                "equipmentTypeKey": equipment_type,
            }

    def _steps(self, steps_config):
        steps, step_order, child_step_id = self._steps_recursive(steps_config, 0, None)
        return steps

    def _steps_recursive(self, steps_config, step_order, child_step_id):
        if not steps_config:
            return [], step_order, child_step_id

        steps_config_agg = [(1, steps_config[0])]

        for step_config in steps_config[1:]:
            (repeats, prev_step_config) = steps_config_agg[-1]
            if prev_step_config == step_config:  # repeated step
                steps_config_agg[-1] = (repeats + 1, step_config)  # type: ignore
            else:
                steps_config_agg.append((1, step_config))

        steps = []
        for repeats, step_config in steps_config_agg:
            step_order = step_order + 1
            if isinstance(step_config, list):
                child_step_id = child_step_id + 1 if child_step_id else 1

                repeat_step_order = step_order
                repeat_child_step_id = child_step_id

                nested_steps, step_order, child_step_id = self._steps_recursive(step_config, step_order, child_step_id)
                steps.append(self._repeat_step(repeat_step_order, repeat_child_step_id, repeats, nested_steps))
            else:
                steps.append(self._interval_step(step_config, child_step_id, step_order))

        return steps, step_order, child_step_id

    def _repeat_step(self, step_order, child_step_id, repeats, nested_steps):
        return {
            "type": "RepeatGroupDTO",
            "stepOrder": step_order,
            "stepType": self.get_step_type("repeat"),
            "childStepId": child_step_id,
            "numberOfIterations": repeats,
            "workoutSteps": nested_steps,
            "smartRepeat": False
        }

    def _interval_step(self, step_config, child_step_id, step_order):
        return WorkoutStep(order=step_order,
                           child_step_id=child_step_id,
                           description=step_config['description'] if 'description' in step_config else None,
                           step_type=step_config['type'] if 'duration' in step_config else None,
                           end_condition=self._end_condition(step_config)['conditionTypeKey'],
                           end_condition_value=step_config['duration'] if 'duration' in step_config else None,
                           target=Target(target=self._target_type(step_config)['workoutTargetTypeKey'],
                                         to_value=self._target_value(step_config, 'min'),
                                         from_value=self._target_value(step_config, 'max')
                                         )
                           ).create_workout_step()

    def _str_is_time(self, string):
        return True if ':' in string else False

    def _str_to_seconds(self, time_string):
        return Duration(str(time_string)).to_seconds()

    def _str_is_distance(self, string):
        return True if 'm' in string.lower() else False

    def _str_to_meters(self, distance_string):
        if 'km' in distance_string.lower():
            return float(distance_string.lower().split('km')[0])*1000.0
        return float(distance_string.lower().split('m')[0])

    def _end_condition(self, step_config):
        duration = step_config.get("duration")
        if duration:
            if self._str_is_time(duration):
                return self.get_end_condition("time")
            elif self._str_is_distance(duration):
                return self.get_end_condition("distance")
        return self.get_end_condition("lap.button")

    def _end_condition_value(self, step_config):
        duration = step_config.get("duration")
        if duration:
            if self._str_is_time(duration):
                return self._str_to_seconds(duration)
            if self._str_is_distance(duration):
                return self._str_to_meters(duration)
        return int(0)

    def _get_target_value(self, target, key):
        target_type = self.target[target]['type']
        target_value = self.target[target][key]

        if self.sport_type[0] == 'running':
            if target_type == "power.zone":
                return int(float(target_value) * self.rFTP)
            elif target_type == "cadence.zone":
                return int(target_value)
            elif target_type == "heart.rate.zone":
                return int(self.fmin + float(target_value) * (self.fmax-self.fmin))
            elif target_type == "speed.zone":
                return float(target_value)
            elif target_type == "pace.zone":
                return float(target_value) * 1000.0 / self.vVO2
            else:
                return int(target_value)
        elif self.sport_type[0] == 'cycling':
            if target_type == "power.zone":
                return int(float(target_value) * self.cFTP)
            else:
                return int(target_value)
        else:
            return int(target_value)

    def _target_type(self, step_config):
        target = step_config.get("target")
        if ">" in target:
            d, target = target.split(">")
        elif "<" in target:
            d, target = target.split("<")

        if not target or (target not in self.target):
            return self.get_target_type("no.target")
        else:
            return self.get_target_type(self.target[target]['type'])

    def _target_value(self, step_config, val):
        target = step_config.get("target")
        if isinstance(target, str):
            target_type = self.target[target]['type']
        else:
            return Duration(str(target[val])).to_seconds()

        if not target:
            return int(0)

        if target not in self.target:
            if ">" in target and target_type == "pace.zone":
                d, target = target.split(">")
                return 1000.0/(1000.0/self._get_target_value(target, key=val) - float(d))
            elif "<" in target and target_type == "pace.zone":
                d, target = target.split("<")
                return 1000.0/(1000.0/self._get_target_value(target, key=val) + float(d))
            else:
                return int(0)
        return self._get_target_value(target, key=val)

    def _equivalent_pace(self, step):
        if isinstance(step['target'], dict):
            target_type = step['target']['type']
        else:
            target_type = self.target[step['target']]['type']

        if target_type == "power.zone":
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')
        elif target_type == "cadence.zone":
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')
        elif target_type == "heart.rate.zone":
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')

            t2 = (round((t2 - self.fmin) / (self.fmax - self.fmin), 2) + 0.06) / self.vVO2 * 1000
            t1 = (round((t1 - self.fmin) / (self.fmax - self.fmin), 2) + 0.06) / self.vVO2 * 1000
        elif target_type == "speed.zone":
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')
        elif target_type == "pace.zone":
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')
        else:
            t2 = 0
            t1 = 0
        return min(t1, t2) + 0.5 * (max(t1, t2) - min(t1, t2))

    def _generate_description(self):
        description = ''
        if self.sport_type[0] == 'running':
            if 'description' in self.config:
                description += self.config.get('description') + '. '
            if self.plan != '':
                description += 'Plan: ' + self.plan + '. '
            description += ('Estimated Duration: ' + str(self.duration) + '; '
                            + str(self.mileage).format('2:2f') + ' km. '
                            + str(round(self.ratio, 2)).format('2:2f') + '% vVO2. '
                            + 'rTSS: ' + str(self.tss).format('2:2f'))
        elif self.sport_type[0] == 'cycling':
            description = "FTP %d, TSS %d, NP %d, IF %.2f" % (self.cFTP, self.tss, self.norm_pwr, self.int_fct)
        if description:
            return description
        return ''

    @staticmethod
    def export_yaml(workout, filename):
        workout_dict = {}
        workout_dict['name'] = workout['workoutName']
        workout_dict['sport'] = workout['sportType']['sportTypeKey']
        workout_dict['description'] = workout['description']
        workout_dict['steps'] = []

        if len(workout['workoutSegments']) > 0:
            for i in range(len(workout['workoutSegments'][0]['workoutSteps'])):
                step_json = workout['workoutSegments'][0]['workoutSteps'][i]

                if step_json['stepType']['stepTypeKey'] != 'repeat':
                    workout_dict["steps"].append(step_extraction(step_json))
                else:
                    for j in range(step_json['numberOfIterations']):
                        for k in range(len(step_json['workoutSteps'])):
                            workout_dict["steps"].append(step_extraction(step_json['workoutSteps'][k]))
        else:
            print(filename)
        with open(filename, 'w') as file:
            yaml.dump(workout_dict, file)


class WorkoutStep:
    def __init__(
        self,
        order,
        child_step_id,
        description,
        step_type,
        end_condition="lap.button",
        end_condition_value=None,
        target=None,
    ):
        """Valid end condition values:
        - distance: '2.0km', '1.125km', '1.6km'
        - time: 0:40, 4:20
        - lap.button
        """
        self.order = order
        self.child_step_id = child_step_id
        self.description = description
        self.step_type = step_type
        self.end_condition = end_condition
        self.end_condition_value = end_condition_value
        self.target = target or Target()

    def end_condition_unit(self):
        if self.end_condition and self.end_condition.endswith("km"):
            return {"unitKey": "kilometer"}
        else:
            return None

    def parsed_end_condition_value(self):
        # distance
        if self.end_condition_value and self.end_condition_value.endswith("km"):
            return int(float(self.end_condition_value.replace("km", "")) * 1000)

        # time
        elif self.end_condition_value and ":" in self.end_condition_value:
            return Duration(self.end_condition_value).to_seconds()
        else:
            return None

    def create_workout_step(self):
        return {
            "type": "ExecutableStepDTO",
            "stepId": None,
            "stepOrder": self.order,
            "childStepId": self.child_step_id,
            "description": self.description,
            "stepType": {
                "stepTypeId": STEP_TYPES[self.step_type],
                "stepTypeKey": self.step_type,
            },
            "endCondition": {
                "conditionTypeKey": self.end_condition,
                "conditionTypeId": END_CONDITIONS[self.end_condition],
            },
            "preferredEndConditionUnit": self.end_condition_unit(),
            "endConditionValue": self.parsed_end_condition_value(),
            "endConditionCompare": None,
            "endConditionZone": None,
            **self.target.create_target(),
        }


class Target:
    def __init__(
            self,
            target="no.target",
            to_value=None,
            from_value=None,
            zone=None
            ):

        self.target = target
        self.to_value = to_value
        self.from_value = from_value
        self.zone = zone

    def create_target(self):
        return {
            "targetType": {
                "workoutTargetTypeId": TARGET_TYPES[self.target],
                "workoutTargetTypeKey": self.target,
            },
            "targetValueOne": self.to_value,
            "targetValueTwo": self.from_value,
            "zoneNumber": self.zone,
        }


class Event(object):
    _EVENT_ID_FIELD = "id"
    _EVENT_NAME_FIELD = "eventName"
    _EVENT_DATE_FIELD = "date"
    _EVENT_LOCATION_FIELD = "location"
    _EVENT_TIME_FIELD = "eventTimeLocal"

    def __init__(
            self,
            config
            ):

        self.name = config['name']
        self.date = date(config['date']['year'], config['date']['month'], config['date']['day'])
        self.url = config['url'] if 'url' in config else None
        self.location = config['location'] if 'location' in config else None
        self.time = config['time'] if 'time' in config else None
        self.distance = config['distance'] if 'distance' in config else None
        self.goal = Duration(config['goal']).to_seconds() if 'goal' in config else None
        self.course = config['course'] if 'course' in config else None
        self.sport = config['sport']

    @staticmethod
    def extract_event_id(event):
        return event[Event._EVENT_ID_FIELD]

    @staticmethod
    def extract_event_name(event):
        return event[Event._EVENT_NAME_FIELD]

    @staticmethod
    def extract_event_date(event):
        return event[Event._EVENT_DATE_FIELD]

    @staticmethod
    def extract_event_location(event):
        return event[Event._EVENT_LOCATION_FIELD]

    @staticmethod
    def extract_event_time(event):
        return event[Event._EVENT_TIME_FIELD]

    @staticmethod
    def print_event_summary(event):
        event_id = Event.extract_event_id(event)
        event_name = Event.extract_event_name(event)
        event_date = Event.extract_event_date(event)
        event_location = Event.extract_event_location(event)
        print("{0} {1:20} {2:10} {3}".format(event_id, event_name, event_location, event_date))

    def create_event(self, event_id=None, workout_id=None):
        return {
            'id': event_id,
            self._EVENT_NAME_FIELD: self.name,
            'date': str(self.date),
            'url': self.url,
            'registrationUrl': None,
            'courseId': self.course,
            'completionTarget': {
                'value': self.distance,
                'unit': 'kilometer',
                'unitType': 'distance'
                },
            self._EVENT_TIME_FIELD: {
                'startTimeHhMm': self.time,
                'timeZoneId': 'Europe/Paris'
                },
            'note': None,
            Workout._WORKOUT_ID_FIELD: workout_id,
            'location': self.location,
            'eventType': self.sport,
            'eventPrivacy': {
                'label': 'PRIVATE',
                'isShareable': False,
                'isDiscoverable': False
                },
            'shareableEventUuid': None,
            'eventCustomization': {
                'customGoal': {
                    'value': self.goal,
                    'unit': 'second',
                    'unitType': 'time'},
                'isPrimaryEvent': None,
                'isTrainingEvent': True},
            'race': True,
            'eventOrganizer': True,
            'subscribed': True
            }
