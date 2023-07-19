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


class Workout(object):
    def __init__(
            self,
            config=[],
            target=[],
            vVO2=Pace('5:00'),
            fmin=60,
            fmax=200,
            rFTP=Power('400w'),
            cFTP=Power('200w'),
            plan=str(''),
            race=date.today()
            ):

        self.sport_type = config[_SPORT].lower() if _SPORT in config else None,
        self.config = config
        self.date = config[_DATE] if _DATE in config else None
        self.target = target
        self.vVO2: Pace = vVO2
        self.fmin = fmin
        self.fmax = fmax
        self.rFTP: Power = rFTP
        self.cFTP: Power = cFTP
        self.plan: str = plan
        self.race = race

        self.duration = timedelta(seconds=0)
        self.sec: float = 0
        self.mileage: float = 0
        self.tss: float = 0
        self.ratio: float = 0
        self.norm_pwr: float = 0
        self.int_fct: float = 0

        flatten_steps = functional.flatten(self.config[_STEPS]) if _STEPS in self.config else []

        if self.sport_type[0] == 'running':
            self.running_values(flatten_steps)
        elif self.sport_type[0] == 'cycling':
            self.cycling_values(flatten_steps)

    def zones(self):
        zones = [0.46, 0.6, 0.7, 0.8, 0.84, 1.0, 1.1]
        hr_zones = [round(self.fmin + (self.fmax - self.fmin) * zone) for zone in zones]
        print('::Heart Rate Zones::')
        for i in range(len(zones)-1):
            print('Zone ', i, ': ', hr_zones[i], '-', hr_zones[i + 1])

        Power.power_zones(zones, self.rFTP)

    def get_workout_name(self):
        if self.sport_type[0] == 'running' and _DESCRIPTION in self.config:
            return str(self.config[_NAME] + '-' + self.config[_DESCRIPTION])
        else:
            return str(self.config[_NAME])

    def get_workout_date(self) -> tuple[date, int, int]:
        if self.date:
            return date(self.date['year'], self.date['month'], self.date['day']), int(0), int(0)
        else:
            workout_name = self.config[_NAME]
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

    def running_values(self, flatten_steps):
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
                    duration_secs = min(round(duration_meters / self._equivalent_pace(step)), 24 * 60 * 60)

                sec = sec + duration_secs  # type: ignore
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

    def cycling_values(self, flatten_steps):
        seconds: float = 0
        xs: list[float] = []

        for step in flatten_steps:
            power: Power | None = Power(str(step.get('power'))) if step.get('power') else None
            power_watts: float = power.to_watts(self.cFTP.power) if power else float(0)

            if WorkoutStep._end_condition_key(step) == 'time':
                duration_secs: float = WorkoutStep._end_condition_value(step)
            else:
                duration_secs = float(0)

            if power_watts and duration_secs:
                seconds = seconds + duration_secs
                xs = functional.concatenate(xs, functional.fill(power_watts, duration_secs))

        self.norm_pwr = math.normalized_power(xs) if xs else float(0)
        self.int_fct = math.intensity_factor(self.norm_pwr, self.cFTP.to_watts(self.cFTP))
        self.tss = math.training_stress_score(seconds, self.norm_pwr, self.cFTP.to_watts(self.cFTP))  # type: ignore

    def _get_target_value(self, target, key):
        if isinstance(target, dict):
            target_type = target[_TYPE]
            target_value: str = target[key] if key in _TARGET else str('')
        else:
            target_type: str = self.target[target][_TYPE]
            target_value: str = self.target[target][key]

        if target_type == 'power.zone':
            if self.sport_type[0] == 'running':
                return Power(target_value).to_watts(ftp=self.rFTP.power)
            elif self.sport_type[0] == 'cycling':
                return Power(target_value).to_watts(ftp=self.cFTP.power)
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

    def _target_type(self, step_config, secondary=False):
        target = step_config.get(_SECONDARY) if secondary else step_config.get(_TARGET)
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

    def _target_value(self, step_config, val, secondary=False):
        target = step_config.get(_SECONDARY) if secondary else step_config.get(_TARGET)
        if isinstance(target, dict):
            target_type = target[_TYPE]
        else:
            target_type = self.target[target][_TYPE]

        if not target:
            return float(0)

        if isinstance(target, dict):
            return self._get_target_value(target, key=val)
        else:
            if target not in self.target:
                if '>' in target and target_type == 'pace.zone':
                    d, target = target.split('>')
                    return 1000.0/(1000.0/self._get_target_value(target, key=val) - float(d))  # type: ignore
                elif '<' in target and target_type == 'pace.zone':
                    d, target = target.split('<')
                    return 1000.0/(1000.0/self._get_target_value(target, key=val) + float(d))  # type: ignore
                else:
                    return float(0)
        return self._get_target_value(target, key=val)

    def _equivalent_pace(self, step):
        if isinstance(step[_TARGET], dict):
            target_type = step[_TARGET][_TYPE]
        else:
            target_type = self.target[step[_TARGET]][_TYPE]

        if (target_type == 'power.zone') or (target_type == 'cadence.zone') or \
           (target_type == 'speed.zone') or (target_type == 'pace.zone'):
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')
        elif target_type == 'heart.rate.zone':
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')

            t2 = (round((t2 - self.fmin) / (self.fmax - self.fmin), 2) + 0.06) * self.vVO2.to_pace()  # type: ignore
            t1 = (round((t1 - self.fmin) / (self.fmax - self.fmin), 2) + 0.06) * self.vVO2.to_pace()  # type: ignore
        else:
            t2 = 0
            t1 = 0
        return min(t1, t2)  # + 0.5 * (max(t1, t2) - min(t1, t2))  # type: ignore

    def _generate_description(self):
        description = ''
        if self.sport_type[0] == 'running':
            if _DESCRIPTION in self.config:
                description += self.config.get(_DESCRIPTION) + '. '
            if self.plan != '':
                description += 'Plan: ' + self.plan + '. '
            description += ('Estimated Duration: ' + str(self.duration) + '; '
                            + str(self.mileage).format('2:2f') + ' km. '
                            + str(round(self.ratio, 2)).format('2:2f') + '% vVO2. '
                            + 'rTSS: ' + str(self.tss).format('2:2f'))
        elif self.sport_type[0] == 'cycling':
            description = 'FTP %d, TSS %d, NP %d, IF %.2f' % (self.cFTP, self.tss, self.norm_pwr, self.int_fct)
        else:
            description = self.config.get(_DESCRIPTION)
        if description:
            return description

    @staticmethod
    def extract_workout_id(workout):
        return workout[_WORKOUT_ID]

    @staticmethod
    def extract_workout_name(workout):
        return workout[_WORKOUT_NAME]

    @staticmethod
    def extract_workout_description(workout):
        return workout[_DESCRIPTION]

    @staticmethod
    def extract_workout_owner_id(workout):
        return workout[_WORKOUT_OWNER_ID]

    @staticmethod
    def print_workout_json(workout):
        print(json.dumps(functional.filter_empty(workout)))

    @staticmethod
    def print_workout_summary(workout):
        workout_id = Workout.extract_workout_id(workout)
        workout_name = Workout.extract_workout_name(workout)
        workout_description = Workout.extract_workout_description(workout)
        print('{0} {1:20} {2}'.format(workout_id, workout_name, workout_description))

    def _steps(self, steps_config):
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

    def create_workout(self, workout_id=None, workout_owner_id=None):
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

    def _repeat_step(self, step_order, child_step_id, repeats, nested_steps, repeatDuration):
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

    def _interval_step(self, step_config, child_step_id, step_order):
        return WorkoutStep(order=step_order,
                           child_step_id=child_step_id,
                           description=step_config[_DESCRIPTION] if _DESCRIPTION in step_config else None,
                           step_type=step_config[_TYPE] if _TYPE in step_config else None,
                           end_condition=WorkoutStep._end_condition(step_config)[_CONDITION_TYPE_KEY],
                           end_condition_value=step_config[_DURATION] if _DURATION in step_config else None,
                           category=step_config[_CATEGORY] if _CATEGORY in step_config else None,
                           exerciseName=step_config[_EXERCISE_NAME] if _EXERCISE_NAME in step_config else None,
                           target=Target(target=self._target_type(step_config)[_WORKOUT_TARGET_KEY],
                                         value_one=self._target_value(step_config, 'min'),
                                         value_two=self._target_value(step_config, 'max'),
                                         secondary=False
                                         ),
                           secondary_target=Target(
                                            target=self._target_type(
                                                                step_config,
                                                                _SECONDARY in step_config)[_WORKOUT_TARGET_KEY],
                                            value_one=self._target_value(step_config, 'min',
                                                                         _SECONDARY in step_config),
                                            value_two=self._target_value(step_config, 'max',
                                                                         _SECONDARY in step_config),
                                            secondary=True
                                            ) if _SECONDARY in step_config else None,
                           weight=step_config[_WEIGHT] if _WEIGHT in step_config else None
                           ).create_workout_step()
