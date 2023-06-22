import json

from garminworkouts.models.workoutstep import WorkoutStep
from garminworkouts.models.duration import Duration
from garminworkouts.models.power import Power
from garminworkouts.models.target import Target
from datetime import date, timedelta
from garminworkouts.utils import functional, math


SPORT_TYPES = {
    "running": 1,
    "trail_running": 1,
    "cycling": 2,
    "gravel_cycling": 2,
    "mountain_biking": 2,
    "swimming": 4,
    "strength_training": 5,
    "cardio_training": 6,
    "yoga": 7,
    "pilates": 8,
    "hiit": 9,
    "other": 3
}


INTENSITY_TYPES = {
    "active": 1,
    "rest": 2,
    "warmup": 3,
    "cooldown": 4,
}


STROKE_TYPES = {
    "any_stroke": 1,         # Cualquiera
    "backstroke": 2,         # Espalda
    "breaststroke": 3,       # Braza
    "drill": 4,              # Tecnica
    "fly": 5,                # Mariposa
    "free": 6,               # Croll
    "individual_medley": 7,  # Estilos
    "mixed": 8,
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

        self.duration = timedelta(seconds=0)
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
            if not WorkoutStep._end_condition(step)['conditionTypeKey'] == 'lap.button':
                if WorkoutStep._end_condition(step)['conditionTypeKey'] == 'time':
                    duration_secs = WorkoutStep._end_condition_value(step)
                    duration_meters = round(duration_secs * self._equivalent_pace(step))
                if WorkoutStep._end_condition(step)['conditionTypeKey'] == 'distance':
                    duration_meters = WorkoutStep._end_condition_value(step)
                    duration_secs = round(duration_meters / self._equivalent_pace(step))

                sec = sec + duration_secs
                meters = meters + duration_meters

        try:
            self.ratio = round(self.vVO2 / (sec / meters * 1000) * 100)
        except ZeroDivisionError:
            self.ratio = 0
        except ValueError:
            self.ratio = 0

        self.duration = timedelta(seconds=sec)
        self.mileage = round(meters/1000, 2)
        self.tss = round(sec/3600 * (self.ratio * 0.89) ** 2 / 100)

    def cycling_values(self, flatten_steps):
        seconds = 0
        xs = []

        for step in flatten_steps:
            power = WorkoutStep._get_power(step)
            power_watts = power.to_watts(self.cFTP) if power else float(0)

            if WorkoutStep._end_condition(step)['conditionTypeKey'] == 'time':
                duration_secs = WorkoutStep._end_condition_value(step)
            else:
                duration_secs = float(0)

            if power_watts and duration_secs:
                seconds = seconds + duration_secs
                xs = functional.concatenate(xs, functional.fill(power_watts, duration_secs))

        self.norm_pwr = math.normalized_power(xs) if xs else float(0)
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
        if self.sport_type[0] == 'running' and 'description' in self.config:
            return self.config['name'] + '-' + self.config['description']
        else:
            return self.config['name']

    def get_workout_date(self):
        if self.date:
            return date(self.date['year'], self.date['month'], self.date['day']), int(0), int(0)
        else:
            workout_name = self.config['name']
            if '_' in workout_name:
                if workout_name.startswith("R"):
                    ind = 1
                    week = -int(workout_name[ind:workout_name.index('_')])
                    day = int(workout_name[workout_name.index('_') + 1:workout_name.index('_') + 2])
                else:
                    ind = 0
                    week = int(workout_name[ind:workout_name.index('_')])
                    day = int(workout_name[workout_name.index('_') + 1:workout_name.index('_') + 2])

                return self.race - timedelta(weeks=week + 1) + timedelta(days=day), week, day
            else:
                return date.today(), int(0), int(0)

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
    def get_sport_type(sport_type):
        return {
                "sportTypeId": SPORT_TYPES[sport_type],
                "sportTypeKey": sport_type,
            }

    @staticmethod
    def get_intensity_type(target_type):
        return {
                "intensityTypeId": INTENSITY_TYPES[target_type],
                "intensityTypeKey": target_type,
            }

    @staticmethod
    def get_stroke_type(stroke_type):
        return {
                "strokeTypeId": STROKE_TYPES[stroke_type],
                "strokeTypeKey": stroke_type,
            }

    @staticmethod
    def get_equipment_type(equipment_type):
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
            "stepType": WorkoutStep.get_step_type("repeat"),
            "childStepId": child_step_id,
            "numberOfIterations": repeats,
            "workoutSteps": nested_steps,
            "smartRepeat": False
        }

    def _interval_step(self, step_config, child_step_id, step_order):
        return WorkoutStep(order=step_order,
                           child_step_id=child_step_id,
                           description=step_config['description'] if 'description' in step_config else None,
                           step_type=step_config['type'] if 'type' in step_config else None,
                           end_condition=WorkoutStep._end_condition(step_config)['conditionTypeKey'],
                           end_condition_value=step_config['duration'] if 'duration' in step_config else None,
                           category=step_config['category'] if 'category' in step_config else None,
                           exerciseName=step_config['exerciseName'] if 'exerciseName' in step_config else None,
                           target=Target(target=self._target_type(step_config)['workoutTargetTypeKey'],
                                         to_value=self._target_value(step_config, 'min'),
                                         from_value=self._target_value(step_config, 'max')
                                         ),
                           secondary_target=Target(
                                            target=self._target_type(
                                                                step_config,
                                                                'secondary' in step_config)['workoutTargetTypeKey'],
                                            to_value=self._target_value(step_config, 'min',
                                                                        'secondary' in step_config),
                                            from_value=self._target_value(step_config, 'max',
                                                                          'secondary' in step_config)
                                            ) if 'secondary' in step_config else None,
                           weight=step_config['weight'] if 'weight' in step_config else None
                           ).create_workout_step()

    def _get_target_value(self, target, key):
        if isinstance(target, dict):
            target_type = target['type']
            target_value = target[key] if key in 'target' else int(0)
        else:
            target_type = self.target[target]['type']
            target_value = self.target[target][key]

        if target_type == "power.zone":
            if self.sport_type[0] == 'running':
                return float(target_value * self.rFTP)
            elif self.sport_type[0] == 'cycling':
                return float(target_value * self.cFTP)
        elif target_type == "cadence.zone":
            return float(target_value)
        elif target_type == "heart.rate.zone":
            return int(self.fmin + float(target_value) * (self.fmax-self.fmin))
        elif target_type == "speed.zone":
            return float(target_value)
        elif target_type == "pace.zone":
            if self.sport_type[0] == 'running':
                return float(target_value * 1000.0 / self.vVO2)
            else:
                return float(target_value)
        else:
            return None

    def _target_type(self, step_config, secondary=False):
        target = step_config.get("secondary") if secondary else step_config.get("target")
        if ">" in target:
            d, target = target.split(">")
        elif "<" in target:
            d, target = target.split("<")

        if isinstance(target, dict):
            return Target.get_target_type(target['type'])

        if not target or (target not in self.target):
            return Target.get_target_type("no.target")
        else:
            return Target.get_target_type(self.target[target]['type'])

    def _target_value(self, step_config, val, secondary=False):
        target = step_config.get("secondary") if secondary else step_config.get("target")
        if isinstance(target, str):
            target_type = self.target[target]['type']
        elif isinstance(target, dict):
            target_type = target['type']
        else:
            return Duration(str(target[val])).to_seconds()

        if not target:
            return float(0)

        if isinstance(target, dict):
            return self._get_target_value(target, key=val)
        else:
            if target not in self.target:
                if ">" in target and target_type == "pace.zone":
                    d, target = target.split(">")
                    return 1000.0/(1000.0/self._get_target_value(target, key=val) - float(d))  # type: ignore
                elif "<" in target and target_type == "pace.zone":
                    d, target = target.split("<")
                    return 1000.0/(1000.0/self._get_target_value(target, key=val) + float(d))  # type: ignore
                else:
                    return float(0)
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

            t2 = (round((t2 - self.fmin) / (self.fmax - self.fmin), 2) + 0.06) / self.vVO2 * 1000  # type: ignore
            t1 = (round((t1 - self.fmin) / (self.fmax - self.fmin), 2) + 0.06) / self.vVO2 * 1000  # type: ignore
        elif target_type == "speed.zone":
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')
        elif target_type == "pace.zone":
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')
        else:
            t2 = 0
            t1 = 0
        return min(t1, t2) + 0.5 * (max(t1, t2) - min(t1, t2))  # type: ignore

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
        else:
            description = self.config.get('description')
        if description:
            return description
        return ''
