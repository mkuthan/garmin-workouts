import json

from garminworkouts.models.workoutstep import WorkoutStep
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from garminworkouts.models.duration import Duration
from garminworkouts.models.target import Target
from datetime import date, timedelta
from garminworkouts.utils import functional, math
from garminworkouts.models.fields import get_sport_type, get_target_type, get_step_type
from garminworkouts.models.fields import _WORKOUT_ID, _WORKOUT_NAME, _DESCRIPTION, _WORKOUT_OWNER_ID
from garminworkouts.models.fields import _WORKOUT_SPORT_TYPE, _WORKOUT_SEGMENTS, _WORKOUT_ORDER, _WORKOUT_STEPS
from garminworkouts.models.fields import _STEP_TYPE, _TYPE, _SPORT, _DATE, _TARGET, _NAME, _SECONDARY, _REPEAT_GROUP
from garminworkouts.models.fields import _DURATION, _WEIGHT, _CONDITION_TYPE_KEY, _CATEGORY, _STEP_ORDER, _EXERCISE_NAME
from garminworkouts.models.fields import _WORKOUT_TARGET_KEY, _STEPS, _REPEAT, _ITERATIONS, _CHILD_STEP_ID
from garminworkouts.models.fields import _END_CONDITION, _END_CONDITION_VALUE
from garminworkouts.models.fields import _PREFERRED_END_CONDITION_UNIT, get_end_condition
import logging


class Workout(object):
    def __init__(
            self,
            config=[],
            target=[],
            vVO2=Pace('5:00'),
            fmin=60,
            fmax=200,
            flt=185,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan=str(''),
            race=date.today()
            ) -> None:

        try:
            self.sport_type: tuple = config[_SPORT].lower() if _SPORT in config else None,
            self.config: dict = config
            self.date: dict | None = config[_DATE] if _DATE in config else None
            self.target: dict = target
            self.vVO2: Pace = vVO2
            self.fmin: int = fmin
            self.fmax: int = fmax
            self.flt: int = flt
            self.rFTP: Power = rFTP
            self.cFTP: Power = cFTP
            self.plan: str = plan
            self.race: date = race

            self.duration = timedelta(seconds=0)
            self.sec: float = 0
            self.mileage: float = 0
            self.tss: float = 0
            self.ratio: float = 0
            self.norm_pwr: float = 0
            self.int_fct: float = 0

            flatten_steps: list = functional.flatten(self.config[_STEPS]) if _STEPS in self.config else []

            if self.sport_type[0] == 'running':
                self.running_values(flatten_steps)
            elif self.sport_type[0] == 'cycling':
                self.cycling_values(flatten_steps)
            elif self.sport_type[0] == 'swimming':
                self.swimming_values(flatten_steps)
            else:
                self.cardio_values(flatten_steps)
            if self.mileage == 0 and self.sec == 0:
                raise ValueError('Null workout')
        except KeyError:
            print(config['name'])
        except ValueError:
            print(config['name'] if 'name' in config else '')

    def zones(self) -> None:
        zones, hr_zones, data = self.hr_zones()
        logging.info('::Heart Rate Zones::')
        logging.info("fmin: %s flt: %s fmax: %s", str(self.fmin), str(self.flt), str(self.fmax))
        for i in range(len(zones)-1):
            logging.info(" Zone %s: %s - %s", i, hr_zones[i], hr_zones[i + 1])

        zones, rpower_zones, cpower_zones, data = Power.power_zones(self.rFTP, self.cFTP)

        logging.info('::Running Power Zones::')
        for i in range(len(zones)-1):
            logging.info(" Zone %s: %s - %s w", i, rpower_zones[i], rpower_zones[i + 1])

        logging.info('::Cycling Power Zones::')
        for i in range(len(zones)-1):
            logging.info(" Zone %s: %s - %s w", i, cpower_zones[i], cpower_zones[i + 1])

    def get_workout_name(self) -> str:
        if self.plan != '' and _DESCRIPTION in self.config:
            return str(self.config[_NAME] + '-' + self.config[_DESCRIPTION])
        else:
            return str(self.config[_NAME])

    def get_workout_date(self) -> tuple[date, int, int]:
        if self.date:
            return date(self.date['year'], self.date['month'], self.date['day']), int(0), int(0)
        else:
            workout_name: str = self.config[_NAME]
            if '_' in workout_name:
                if workout_name.startswith('R'):
                    ind = 1
                    week: int = -int(workout_name[ind:workout_name.index('_')])
                    day = int(workout_name[workout_name.index('_') + 1:workout_name.index('_') + 2])
                else:
                    ind = 0
                    week = int(workout_name[ind:workout_name.index('_')])
                    day = int(workout_name[workout_name.index('_') + 1:workout_name.index('_') + 2])

                return self.race - timedelta(weeks=week + 1) + timedelta(days=day), week, day
            else:
                return date.today(), int(0), int(0)

    def running_values(self, flatten_steps) -> None:
        sec: float = 0
        meters = 0
        duration_secs = 0
        duration_meters = 0

        for step in flatten_steps:
            key: str = WorkoutStep._end_condition_key(WorkoutStep._end_condition(step))
            duration: float = WorkoutStep._end_condition_value(step)
            if not key == 'lap.button':
                if key == 'time':
                    duration_secs: float = duration
                    duration_meters = round(duration_secs * self._equivalent_pace(step))
                if key == 'distance':
                    duration_meters: float = duration
                    try:
                        duration_secs = min(round(duration_meters / self._equivalent_pace(step)), 24 * 60 * 60)
                    except ZeroDivisionError:
                        duration_secs = float(0)

                sec = sec + duration_secs
                meters: float = meters + duration_meters

        try:
            self.ratio = float(round(meters / sec / self.vVO2.to_pace() * 100))
        except ZeroDivisionError:
            self.ratio = float(0)
        except ValueError:
            self.ratio = float(0)

        self.sec = sec
        self.duration = timedelta(seconds=sec)
        self.mileage: float = round(meters/1000, 2)
        self.tss: float = round(sec/3600 * (self.ratio * 0.89) ** 2 / 100)

    def cycling_values(self, flatten_steps) -> None:
        sec: float = 0
        meters = 0
        duration_secs = 0
        duration_meters = 0
        seconds: float = 0
        xs: list[float] = []

        for step in flatten_steps:
            power: Power | None = Power(str(step.get('power'))) if step.get('power') else None
            power_watts: float = power.to_watts(self.cFTP.power[:-1]) if power else float(0)

            key: str = WorkoutStep._end_condition_key(WorkoutStep._end_condition(step))
            duration: float = WorkoutStep._end_condition_value(step)
            if not key == 'lap.button':
                if key == 'time':
                    duration_secs: float = duration
                    duration_meters = round(duration_secs * self._equivalent_pace(step))
                if key == 'distance':
                    duration_meters: float = duration
                    try:
                        duration_secs = min(round(duration_meters / self._equivalent_pace(step)), 24 * 60 * 60)
                    except ZeroDivisionError:
                        duration_secs = float(0)

                sec = sec + duration_secs
                meters: float = meters + duration_meters

            if power_watts and duration_secs:
                seconds = seconds + duration_secs
                xs = functional.concatenate(xs, functional.fill(power_watts, duration_secs))  # type: ignore

        self.sec = sec
        self.duration = timedelta(seconds=sec)
        self.mileage: float = round(meters/1000, 2)
        self.norm_pwr = math.normalized_power(xs) if xs else float(0)
        self.int_fct = math.intensity_factor(self.norm_pwr, self.cFTP.to_watts(self.cFTP.power[:-1]))
        self.tss = math.training_stress_score(seconds, self.norm_pwr, self.cFTP.to_watts(self.cFTP.power[:-1]))

    def swimming_values(self, flatten_steps) -> None:
        sec: float = 0
        meters = 0
        duration_secs = 0
        duration_meters = 0

        for step in flatten_steps:
            key: str = WorkoutStep._end_condition_key(WorkoutStep._end_condition(step))
            duration: float = WorkoutStep._end_condition_value(step)
            if not key == 'lap.button':
                if key == 'time':
                    duration_secs: float = duration
                    duration_meters = round(duration_secs * self._equivalent_pace(step))
                if key == 'distance':
                    duration_meters: float = duration
                    try:
                        duration_secs = min(round(duration_meters / self._equivalent_pace(step)), 24 * 60 * 60)
                    except ZeroDivisionError:
                        duration_secs = float(0)

                sec = sec + duration_secs
                meters: float = meters + duration_meters

        try:
            self.ratio = float(round(meters / sec / self.vVO2.to_pace() * 100))
        except ZeroDivisionError:
            self.ratio = float(0)
        except ValueError:
            self.ratio = float(0)

        self.sec = sec
        self.duration = timedelta(seconds=sec)
        self.mileage: float = round(meters/1000, 2)
        self.tss: float = round(sec/3600 * (self.ratio * 0.89) ** 2 / 100)

    def cardio_values(self, flatten_steps) -> None:
        sec: float = 0
        duration_secs = 0
        duration_reps = 0
        reps = 0

        for step in flatten_steps:
            key: str = WorkoutStep._end_condition_key(WorkoutStep._end_condition(step))
            duration: float = WorkoutStep._end_condition_value(step)
            if not key == 'lap.button':
                if key == 'time':
                    duration_secs: float = duration
                    duration_reps = 0
                if key == 'reps':
                    duration_reps: float = duration
                    duration_secs = float(0)

                sec += duration_secs
                reps += duration_reps

        self.ratio = float(0)

        self.sec = sec
        self.duration = timedelta(seconds=sec)
        self.mileage: float = len(flatten_steps) if sec == 0 and reps == 0 else reps
        self.tss: float = round(sec/3600 * (self.ratio * 0.89) ** 2 / 100)

    def zone_extractor(self, target, key):
        if isinstance(target, dict):
            target_type = target[_TYPE]
            target_value: str = target[key] if key in _TARGET else str('')
        else:
            target_type: str = self.target[target][_TYPE]
            target_value: str = self.target[target][key] if key in self.target[target] else '0'

        if 'zone' in self.target[target]:
            z = int(self.target[target]['zone'])
            if target_type == 'heart.rate.zone':
                zones, hr_zones, data = self.hr_zones()
                t = {'min': zones[z], 'max': zones[z + 1]}
                target_value = str(t[key])
            elif target_type == 'power.zone':
                zones, rpower_zones, cpower_zones, data = Power.power_zones(self.rFTP, self.cFTP)
                t = {'min': zones[z - 1], 'max': zones[z]}
                target_value = str(t[key])
        return target_type, target_value

    def _get_target_value(self, target, key) -> float:
        target_type, target_value = self.zone_extractor(target, key)
        if target_type == 'power.zone':
            if self.sport_type[0] == 'running':
                return Power(target_value).to_watts(ftp=self.rFTP.power[:-1])
            elif self.sport_type[0] == 'cycling':
                return Power(target_value).to_watts(ftp=self.cFTP.power[:-1])
            else:
                return float(0)
        elif target_type == 'cadence.zone':
            return float(target_value)
        elif target_type == 'heart.rate.zone':
            return float(int(self.fmin + float(target_value) * (self.fmax-self.fmin)))
        elif target_type == 'speed.zone':
            return float(target_value)
        elif target_type == 'pace.zone':
            if self.sport_type[0] == 'running':
                return Pace(target_value).to_pace(vVO2=self.vVO2.pace)
            else:
                return float(target_value)
        else:
            return float(0)

    def _target_type(self, step_config, secondary=False) -> dict:
        target: str = step_config.get(_SECONDARY) if secondary else step_config.get(_TARGET)
        d: str = ''
        if '>' in target:
            d, target = target.split('>')
        elif '<' in target:
            d, target = target.split('<')

        if isinstance(target, dict):
            return get_target_type(target[_TYPE])

        if not target or (target not in self.target):
            return get_target_type('no.target')
        else:
            return get_target_type(self.target[target][_TYPE])

    def _target_variations(self, target: str, target_type: str, val: str) -> float:
        d: str = ''
        if '>' in target and target_type == 'pace.zone':
            d, target = target.split('>')
            return 1000.0/(1000.0/self._get_target_value(target, key=val) - float(d))
        elif '<' in target and target_type == 'pace.zone':
            d, target = target.split('<')
            return 1000.0/(1000.0/self._get_target_value(target, key=val) + float(d))
        elif '>' in target and target_type == 'heart.rate.zone':
            d, target = target.split('>')
            s: float = ((self._get_target_value(target, key=val) - self.fmin) / (self.fmax - self.fmin) + 0.06
                        ) * self.vVO2.to_pace()
            s = 1000.0/(1000.0/s - float(d))
            return round((s/self.vVO2.to_pace()-0.06)*(self.fmax - self.fmin) + self.fmin)
        elif '<' in target and target_type == 'heart.rate.zone':
            d, target = target.split('<')
            s: float = ((self._get_target_value(target, key=val) - self.fmin) / (self.fmax - self.fmin) + 0.06
                        ) * self.vVO2.to_pace()
            s = 1000.0/(1000.0/s + float(d))
            return round((s/self.vVO2.to_pace()-0.06)*(self.fmax - self.fmin) + self.fmin)
        else:
            return float(0)

    def _target_value(self, step_config, val, secondary=False) -> float:
        target: str = step_config.get(_SECONDARY) if secondary else step_config.get(_TARGET)
        d: str = ''
        if isinstance(target, dict):
            target_type: str = target[_TYPE]
        else:
            target_i: str = ''
            if '>' in target:
                d, target_i = target.split('>')
                target_type = self.target[target_i][_TYPE]
            elif '<' in target:
                d, target_i = target.split('<')
                target_type = self.target[target_i][_TYPE]
            else:
                target_type = self.target[target][_TYPE]

        if not target:
            return float(0)

        if isinstance(target, dict):
            return self._get_target_value(target, key=val)
        else:
            if target not in self.target:
                return self._target_variations(target, target_type, val)
        return self._get_target_value(target, key=val)

    def hr_zones(self) -> tuple[list[float], list[int], list[dict]]:
        zones: list[float] = [0.46, 0.6, 0.7, 0.8, (self.flt - self.fmin)/(self.fmax - self.fmin), 1.0, 1.1]
        hr_zones: list[int] = [round(self.fmin + (self.fmax - self.fmin) * zone) for zone in zones]

        data: list[dict] = [{
            "changeState": "CHANGED",
            "trainingMethod": "HR_RESERVE",
            "lactateThresholdHeartRateUsed": hr_zones[4],
            "maxHeartRateUsed": self.fmax,
            "restingHrAutoUpdateUsed": False,
            "sport": "DEFAULT",
            "trainingMethod": "HR_RESERVE",
            "zone1Floor": hr_zones[0],
            "zone2Floor": hr_zones[1],
            "zone3Floor": hr_zones[2],
            "zone4Floor": hr_zones[3],
            "zone5Floor": hr_zones[4]}]

        return zones, hr_zones, data

    def _equivalent_pace(self, step) -> float:
        if isinstance(step[_TARGET], dict):
            target_type = step[_TARGET][_TYPE]
        else:
            target: str = step[_TARGET]
            d: str = ''
            if '>' in target:
                d, target = target.split('>')
            elif '<' in target:
                d, target = target.split('<')
            target_type: str = self.target[target][_TYPE]

        if (target_type == 'cadence.zone') or \
           (target_type == 'speed.zone') or (target_type == 'pace.zone'):
            t2: float = self._target_value(step, 'max')
            t1: float = self._target_value(step, 'min')
        elif target_type == 'heart.rate.zone':
            if 'zone' in step['target']:
                zones, hr_zones, data = self.hr_zones()

                z = int(step['target']['zone'])
                t2 = hr_zones[z + 1]
                t1 = hr_zones[z]
            else:
                t2 = self._target_value(step, 'max')
                t1 = self._target_value(step, 'min')

            t2 = (round((t2 - self.fmin) / (self.fmax - self.fmin), 2) + 0.06) * self.vVO2.to_pace()
            t1 = (round((t1 - self.fmin) / (self.fmax - self.fmin), 2) + 0.06) * self.vVO2.to_pace()
        elif target_type == 'power.zone':
            if 'zone' in step['target']:
                zones, rpower_zones, cpower_zones, data = Power.power_zones(self.rFTP, self.cFTP)

                z = int(step['target']['zone'])
                t2 = rpower_zones[z]
                t1 = rpower_zones[z - 1]
            else:
                t2 = self._target_value(step, 'max')
                t1 = self._target_value(step, 'min')

            t2 = 0.0
            t1 = 0.0
        else:
            t2 = 0.0
            t1 = 0.0
        return min(t1, t2)  # + 0.5 * (max(t1, t2) - min(t1, t2))

    def _generate_description(self):
        description: str = ''
        if self.sport_type[0] == 'running':
            if self.plan == '' and _DESCRIPTION in self.config:
                description += self.config[_DESCRIPTION] + '. '
            if self.plan != '':
                description += 'Plan: ' + self.plan + '. '
            description += ('Estimated Duration: ' + str(self.duration) + '; '
                            + str(self.mileage).format('2:2f') + ' km. '
                            + str(round(self.ratio, 2)).format('2:2f') + '% vVO2. '
                            + 'rTSS: ' + str(self.tss).format('2:2f'))
        elif self.sport_type[0] == 'cycling':
            description = 'FTP %d, TSS %d, NP %d, IF %.2f' % (self.cFTP, self.tss, self.norm_pwr, self.int_fct)
        else:
            description = self.config[_DESCRIPTION]
        if description:
            return description

    @staticmethod
    def extract_workout_id(workout) -> str:
        return workout[_WORKOUT_ID]

    @staticmethod
    def extract_workout_name(workout) -> str:
        return workout[_WORKOUT_NAME]

    @staticmethod
    def extract_workout_description(workout) -> str:
        return workout[_DESCRIPTION]

    @staticmethod
    def extract_workout_owner_id(workout) -> str:
        return workout[_WORKOUT_OWNER_ID]

    @staticmethod
    def print_workout_json(workout) -> None:
        print(json.dumps(functional.filter_empty(workout)))

    @staticmethod
    def print_workout_summary(workout) -> None:
        workout_id: str = Workout.extract_workout_id(workout)
        workout_name: str = Workout.extract_workout_name(workout)
        workout_description: str = Workout.extract_workout_description(workout)
        print('{0} {1:20} {2}'.format(workout_id, workout_name, workout_description))

    def _steps(self, steps_config) -> list:
        steps, step_order, child_step_id, repeatDuration = self._steps_recursive(steps_config, 0, None)
        return steps

    def _steps_recursive(self, steps_config, step_order, child_step_id):
        repeatDuration = None
        if not steps_config:
            return [], step_order, child_step_id, repeatDuration

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

                repeatDuration = step_config[0]['repeatDuration'] if 'repeatDuration' in step_config[0] else None,
                repeatDuration = repeatDuration[0]

                nested_steps, step_order, child_step_id, amrat = self._steps_recursive(
                    step_config, step_order, child_step_id)
                steps.append(self._repeat_step(repeat_step_order, repeat_child_step_id, repeats, nested_steps,
                                               repeatDuration))
            else:
                steps.append(self._interval_step(step_config, child_step_id, step_order))

        return steps, step_order, child_step_id, repeatDuration

    def create_workout(self, workout_id=None, workout_owner_id=None) -> dict:
        return {
            _WORKOUT_ID: workout_id,
            _WORKOUT_OWNER_ID: workout_owner_id,
            _WORKOUT_NAME: self.get_workout_name(),
            _DESCRIPTION: self._generate_description(),
            _WORKOUT_SPORT_TYPE: get_sport_type(self.sport_type[0]),
            _WORKOUT_SEGMENTS: [
                {
                    _WORKOUT_ORDER: 1,
                    _WORKOUT_SPORT_TYPE: get_sport_type(self.sport_type[0]),
                    _WORKOUT_STEPS: self._steps(self.config[_STEPS])
                }
            ],
            "estimatedDurationInSecs": self.sec if self.sec > 0 else None,
            "estimatedDistanceInMeters": self.mileage * 1000 if self.mileage > 0 else None,
        }

    def _repeat_step(self, step_order, child_step_id, repeats, nested_steps, repeatDuration) -> dict:
        return {
            _TYPE: _REPEAT_GROUP,
            _STEP_ORDER: step_order,
            _STEP_TYPE: get_step_type('repeat'),
            _CHILD_STEP_ID: child_step_id,
            _ITERATIONS: repeats if not repeatDuration else None,
            _WORKOUT_STEPS: nested_steps,
            _REPEAT: False,
            _END_CONDITION: get_end_condition('time') if repeatDuration else None,
            _PREFERRED_END_CONDITION_UNIT: WorkoutStep.end_condition_unit('time') if repeatDuration else None,
            _END_CONDITION_VALUE: Duration(repeatDuration).to_seconds() if repeatDuration else None,
        }

    def _interval_step(self, step_config, child_step_id, step_order) -> dict:
        return WorkoutStep(order=step_order,
                           child_step_id=child_step_id,
                           description=step_config[_DESCRIPTION] if _DESCRIPTION in step_config else None,
                           step_type=step_config[_TYPE] if _TYPE in step_config else None,
                           end_condition=WorkoutStep._end_condition(step_config)[_CONDITION_TYPE_KEY],
                           end_condition_value=step_config[_DURATION] if _DURATION in step_config else None,
                           category=step_config[_CATEGORY] if _CATEGORY in step_config else None,
                           exerciseName=step_config[_EXERCISE_NAME] if _EXERCISE_NAME in step_config else None,
                           target=Target(target=self._target_type(step_config)[_WORKOUT_TARGET_KEY],
                                         value_one=self._target_value(
                                             step_config, 'min'),
                                         value_two=self._target_value(
                                             step_config, 'max'),
                                         zone=self._target_value(
                                             step_config, 'zone') if 'zone' in step_config else None,
                                         secondary=False
                                         ),
                           secondary_target=Target(
                                            target=self._target_type(
                                                                step_config,
                                                                _SECONDARY in step_config)[_WORKOUT_TARGET_KEY],
                                            value_one=self._target_value(step_config,
                                                                         'min',
                                                                         _SECONDARY in step_config
                                                                         ),
                                            value_two=self._target_value(step_config,
                                                                         'max',
                                                                         _SECONDARY in step_config
                                                                         ),
                                            zone=self._target_value(step_config,
                                                                    'zone',
                                                                    _SECONDARY in step_config
                                                                    ) if 'zone' in step_config else None,
                                            secondary=True
                                            ) if _SECONDARY in step_config else None,
                           weight=step_config[_WEIGHT] if _WEIGHT in step_config else None
                           ).create_workout_step()
