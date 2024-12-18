import json
import math
from typing import Any
from garminworkouts.models.workoutstep import WorkoutStep
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from garminworkouts.models.duration import Duration
from garminworkouts.models.target import Target
from datetime import date, timedelta
from garminworkouts.utils.functional import concatenate, flatten, fill, filter_empty
from garminworkouts.utils.math import normalized_power, intensity_factor, training_stress_score
from garminworkouts.models.date import get_date
from garminworkouts.models.fields import (get_sport_type, get_target_type, get_step_type,
                                          _WORKOUT_ID, _WORKOUT_NAME, _DESCRIPTION, _WORKOUT_OWNER_ID,
                                          _WORKOUT_SPORT_TYPE, _WORKOUT_SEGMENTS, _WORKOUT_ORDER, _WORKOUT_STEPS,
                                          _STEP_TYPE, _TYPE, _SPORT, _DATE, _TARGET, _NAME, _SECONDARY,
                                          _DURATION, _WEIGHT, _CONDITION_TYPE_KEY, _CATEGORY, _STEP_ORDER,
                                          _EXERCISE_NAME, _WORKOUT_TARGET_KEY, _STEPS, _REPEAT, _ITERATIONS,
                                          _CHILD_STEP_ID, _SUBSPORT, _END_CONDITION, _END_CONDITION_VALUE, _AUTHOR,
                                          _PREFERRED_END_CONDITION_UNIT, _WORKOUT_SUBSPORT_TYPE, _ESTIMATED_DURATION,
                                          _ESTIMATED_DISTANCE, _AVG_SPEED, _REPEAT_DURATION, _REPEAT_GROUP,
                                          get_estimate, get_pool, get_end_condition)
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
            race=None
    ) -> None:

        self.config: Any = config
        if bool(config):
            self.sport_type = config.get(_SPORT, '').lower()
            self.subsport: Any = config.get(_SUBSPORT, None)
            self.date: Any = config.get(_DATE, None)
            flatten_steps = flatten(config.get(_STEPS, []))
        else:
            self.sport_type: str = ''
            self.subsport = None
            self.date = None
            flatten_steps: list[Any] = []

        self.target: Any = target
        self.vVO2: Pace = vVO2
        self.fmin: int = fmin
        self.fmax: int = fmax
        self.flt: int = flt
        self.rFTP: Power = rFTP
        self.cFTP: Power = cFTP
        self.plan: str = plan
        self.race: date | None = race
        self.duration = timedelta(seconds=0)
        self.sec = 0
        self.mileage = 0
        self.tss = 0
        self.ratio = 0
        self.norm_pwr = 0
        self.int_fct = 0
        if self.sport_type == 'running':
            self.running_values(flatten_steps)
        elif self.sport_type == 'cycling':
            self.cycling_values(flatten_steps)
        elif self.sport_type == 'swimming':
            self.swimming_values(flatten_steps)
        else:
            self.cardio_values(flatten_steps)

        self.training_load()

        if bool(config) and self.mileage == 0 and self.sec == 0 and self.reps == 0:
            raise ValueError('Null workout')

    @staticmethod
    def load_metrics(workouts):
        mileage: list[float] = [float(0) for _ in range(24, -11, -1)]
        duration: list[timedelta] = [timedelta(seconds=0) for i in range(24, -11, -1)]
        tss: list[float] = [float(0) for _ in range(24, -11, -1)]
        ECOs: list[float] = [float(0) for _ in range(24, -11, -1)]
        Rdist = [0] * 8
        Rdists = [[0] * 8 for _ in range(24, -11, -1)]

        day_min: date | None = None
        day_max: date | None = None

        for workout in workouts:
            workout_name: str = workout.get_workout_name()
            day_d, week, _ = workout.get_workout_date()
            if day_min is None:
                day_min = day_d
            if day_max is None:
                day_max = day_d
            if day_min > day_d:
                day_min = day_d
            if day_max < day_d:
                day_max = day_d
            mileage[week] += workout.mileage
            duration[week] += workout.duration
            tss[week] += + workout.tss * workout.duration.seconds
            ECOs[week] += workout.ECOs
            Rdist = [r + w_r for r, w_r in zip(Rdist, workout.Rdist)]
            Rdists[week] = [r + w_r for r, w_r in zip(Rdists[week], workout.Rdist)]

            print(workout_name + ' -',
                  str(round(workout.mileage, 2)) + ' km -',
                  str(workout.duration) + ' -',
                  str(round(workout.ECOs, 2)) + ' ECOs')

        logging.info('From ' + str(day_min) + ' to ' + str(day_max))
        for i in range(24, -11, -1):
            if mileage[i] > float(0):
                logging.info('Week ' + str(i) + ': '
                             + str(round(mileage[i], 2)) + ' km - '
                             + 'Duration: ' + str(duration[i]) + ' - '
                             + 'ECOs: ' + str(round(ECOs[i], 2)))

        return mileage, duration, tss, ECOs, Rdist, Rdists, day_min, day_max

    def zones(self) -> None:
        zones, hr_zones, _ = self.hr_zones()
        logging.info('::Heart Rate Zones::')
        logging.info(f"fmin: {self.fmin} flt: {self.flt} fmax: {self.fmax}")
        for i in range(len(zones)):
            logging.info(f" Zone {i}: {hr_zones[i]} - {hr_zones[i + 1] if i + 1 < len(hr_zones) else 'max'}")

        zones, rpower_zones, cpower_zones, _ = Power.power_zones(self.rFTP, self.cFTP)
        logging.info('::Running Power Zones::')
        for i in range(len(rpower_zones)):
            logging.info(
                f" Zone {i}: {rpower_zones[i]} - {rpower_zones[i + 1] if i + 1 < len(rpower_zones) else 'max'} w")

        logging.info('::Cycling Power Zones::')
        for i in range(len(cpower_zones)):
            logging.info(
                f" Zone {i}: {cpower_zones[i]} - {cpower_zones[i + 1] if i + 1 < len(cpower_zones) else 'max'} w")

    def get_workout_name(self) -> str:
        if '_' not in self.config.get(_NAME, ''):
            return str(self.config.get(_NAME))
        else:
            le = 25
            description: str = self.config.get(_DESCRIPTION, '')
            if not description:
                description = ''
            description = description.replace("W1-", "").replace("W2-", "").replace("W3-", "").replace(" + ", "+")
            if (self.plan != '') and (_DESCRIPTION in self.config) and (description is not None) and \
               (len(description) < le) and ('\n' not in description):
                return f"{self.config.get(_NAME, '')}-{description}"
            elif len(description) >= le:
                return f"{self.config.get(_NAME)}-{description.split(' ')[0]}"
            else:
                return str(self.config.get(_NAME))

    def get_workout_date(self) -> tuple[date, int, int]:
        workout_name: str = self.config.get(_NAME, '')
        return get_date(workout_name, self.race, self.date)

    def running_values(self, flatten_steps) -> None:
        sec = 0
        meters = 0
        for step in flatten_steps:
            duration_secs, duration_meters = self.extract_step_duration(step)
            sec += duration_secs
            meters += duration_meters

        try:
            self.ratio: float = round(meters / sec / self.vVO2.to_pace() * 100, 2)
        except ZeroDivisionError:
            self.ratio = 0

        self.sec: float = sec
        self.duration = timedelta(seconds=sec)
        self.mileage = round(meters / 1000, 2)
        self.reps = 0
        self.tss = round(sec / 3600 * (self.ratio) ** 2 / 100, 0)
        try:
            self.pace: float = self.sec/self.mileage
        except ZeroDivisionError:
            self.pace = 0

    def cycling_values(self, flatten_steps) -> None:
        sec: float = 0
        meters = 0
        duration_secs = 0
        duration_meters = 0
        seconds: float = 0
        xs: list[float] = []

        cFTP_power: float = float(self.cFTP.power[:-1])

        for step in flatten_steps:
            duration_secs, duration_meters = self.extract_step_duration(step)
            sec = sec + duration_secs
            meters: float = meters + duration_meters

            target_type = self.extract_target(step).get('type')
            if target_type == 'power.zone':
                _, _, cpower_zones, _ = Power.power_zones(self.rFTP, self.cFTP)
                z = int(step.get('target').get('zone'))
                power_watts: float = cpower_zones[z]
            else:
                power_watts = 0

            if power_watts and duration_secs:
                seconds = seconds + duration_secs
                xs = concatenate(xs, fill(power_watts, duration_secs))  # type: ignore

        self.sec = sec
        self.duration = timedelta(seconds=sec)
        self.mileage: float = round(meters/1000, 2)
        self.reps = 0
        try:
            self.norm_pwr: float = float(normalized_power(xs))
        except ValueError:
            self.norm_pwr = float(0)

        self.int_fct = float(intensity_factor(self.norm_pwr, cFTP_power))
        self.tss = float(training_stress_score(seconds, self.norm_pwr, cFTP_power))

    def swimming_values(self, flatten_steps) -> None:
        sec: float = 0
        meters = 0
        duration_secs = 0
        duration_meters = 0

        for step in flatten_steps:
            duration_secs, duration_meters = self.extract_step_duration(step)
            sec += duration_secs
            meters += duration_meters

        self.sec = sec
        self.duration = timedelta(seconds=sec)
        self.mileage: float = round(meters/1000, 2)
        self.reps = 0

    def cardio_values(self, flatten_steps) -> None:
        sec: float = 0
        duration_secs = 0
        duration_reps = 0
        reps = 0

        for step in flatten_steps:
            assert step.get('type') != 'run'
            key: str = WorkoutStep._end_condition_key(WorkoutStep._end_condition(step))
            duration: float = WorkoutStep._end_condition_value(step)
            match key:
                case 'time':
                    duration_secs: float = duration
                    duration_reps = float(0)
                case 'reps':
                    duration_reps: float = duration
                    duration_secs = float(0)
                case _:
                    duration_reps = float(0)
                    duration_secs = float(0)
            sec += duration_secs
            reps += duration_reps

        self.ratio = float(0)
        self.sec = sec
        self.duration = timedelta(seconds=sec)
        self.mileage = 0
        self.reps: float = len(flatten_steps) if sec == 0 and reps == 0 else reps

    def training_load(self):
        self.ECOs = 0
        intensity_factor_list = []
        Rdist = [0] * 8

        if len(self.config) > 0 and self.config.get('steps') is not None:
            for step in self.config.get('steps'):
                ECOs, intensity_factor_list, Rdist = self.process_step(step, intensity_factor_list, Rdist)
                self.ECOs += self.calculate_ECOs(ECOs, intensity_factor_list)
        self.Rdist = Rdist

    def process_step(self, step, intensity_factor_list, Rdist):
        interval, recovery, rest, warmup, cooldown, other, maxIF, ECOs = 0, 0, 0, 0, 0, 0, 0, 0

        if not isinstance(step, list):
            step = [step]

        for substep in step:
            duration_secs, duration_meters = self.extract_step_duration(substep)
            c, intensity_factor, Rdist = self.get_intensity_factor(duration_secs, duration_meters, Rdist)
            maxIF = max(maxIF, intensity_factor)
            intensity_factor_list.append(intensity_factor)
            ECOs += round(c * duration_secs * intensity_factor / 60, 0)
            interval, recovery, rest, warmup, cooldown, other = self.update_durations(substep, duration_secs, interval,
                                                                                      recovery, rest, warmup, cooldown,
                                                                                      other)

        if len(step) > 1:
            ECOs *= 1 - self.calculate_p(interval, recovery, rest, warmup, cooldown, other, maxIF) / 100

        return ECOs, intensity_factor_list, Rdist

    def get_intensity_factor(self, duration_secs, duration_meters, Rdist):
        match self.sport_type:
            case 'running':
                c = 1.0
                intensity_factor, Rdist = self.intensity_factor(
                    round(duration_meters / duration_secs / self.vVO2.to_pace(), 2),
                    duration_secs, Rdist) if duration_secs > 0 else (0, Rdist)
            case 'cycling':
                c = 0.5
                intensity_factor = 1.0
            case 'swimming':
                c = 0.75
                intensity_factor = 1.0
            case _:
                c = 0.4
                intensity_factor = 1.0
        return c, intensity_factor, Rdist

    def update_durations(self, substep, duration_secs, interval, recovery, rest, warmup, cooldown, other):
        match substep.get('type'):
            case 'interval':
                interval += duration_secs
            case 'recovery':
                recovery += duration_secs
            case 'rest':
                rest += duration_secs
            case 'warmup':
                warmup += duration_secs
            case 'cooldown':
                cooldown += duration_secs
            case _:
                other += duration_secs
        return interval, recovery, rest, warmup, cooldown, other

    def calculate_p(self, interval, recovery, rest, warmup, cooldown, other, maxIF):
        if (recovery + rest) == 0:
            return 0.0
        elif maxIF <= 3.0:
            return (recovery + rest) / (interval + recovery + rest + warmup + cooldown + other) * 100
        else:
            D = interval / (recovery + rest)
            if maxIF <= 5.0:
                return 20.204 * math.log(D) - 50.791
            elif maxIF <= 9.0:
                return 40.257 * math.log(D) - 35.627
            elif maxIF <= 15.0:
                return 37.085 * math.log(D) - 6.219
            else:
                return 89.204 * D - 270532

    def calculate_ECOs(self, ECOs, intensity_factor_list):
        if len(intensity_factor_list) == 1:
            return ECOs
        else:
            return ECOs * (1 + intensity_factor_list[-1]/intensity_factor_list[-2] / 10
                           ) if intensity_factor_list[-2] > 0 else ECOs

    def intensity_factor(self, v: float, duration_secs, Rdist):
        if v < 0.5:
            c = 0.0
        elif v >= 0.5 and v < 0.65:  # R0
            c = 1.0
            Rdist[0] += duration_secs
        elif v >= 0.65 and v < 0.75:  # R1
            c = 2.0
            Rdist[1] += duration_secs
        elif v >= 0.75 and v < 0.875:  # R2
            c = 3.0
            Rdist[2] += duration_secs
        elif v >= 0.875 and v < 0.95:  # R3
            c = 5.0
            Rdist[3] += duration_secs
        elif v >= 0.95 and v < 1.05:  # R3+
            c = 9.0
            Rdist[4] += duration_secs
        elif v >= 1.05 and v < 1.20:  # R4
            c = 15.0
            Rdist[5] += duration_secs
        elif v >= 1.20 and v < 1.50:  # R5
            c = 40.0
            Rdist[6] += duration_secs
        else:
            c = 50.0  # R6
            Rdist[7] += duration_secs
        return c, Rdist

    def extract_step_duration(self, step) -> tuple[float, float]:
        end_condition: dict = WorkoutStep._end_condition(step)
        key: str = WorkoutStep._end_condition_key(end_condition)
        duration: int = WorkoutStep._end_condition_value(step)

        if key == 'time':
            duration_secs: int = duration
            duration_meters: int = round(duration_secs * self.equivalent_pace(step))
        elif key == 'distance':
            duration_meters = duration
            try:
                duration_secs = min(round(duration_meters / self.equivalent_pace(step)), 24 * 60 * 60)
            except ZeroDivisionError:
                duration_secs = 0
        else:
            duration_secs = 0
            duration_meters = 0
        return duration_secs, duration_meters

    def equivalent_pace(self, step) -> float:
        t2: float = 0.0
        t1: float = 0.0

        target = self.extract_target(step)
        target_type: str = self.extract_target_type(target)

        if target_type == 'speed.zone':
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')
        elif target_type == 'pace.zone':
            t2 = self._target_value(step, 'max')
            t1 = self._target_value(step, 'min')
        elif target_type == 'heart.rate.zone':
            if 'zone' in target:
                _, hr_zones, _ = self.hr_zones()
                z = int(target.get('zone'))
                t2 = self.convert_HR_to_pace(hr_zones[z + 1])
                t1 = self.convert_HR_to_pace(hr_zones[z])
            else:
                t2 = self.convert_HR_to_pace(self._target_value(step, 'max'))
                t1 = self.convert_HR_to_pace(self._target_value(step, 'min'))
        else:
            t2 = 0.0
            t1 = 0.0

        return min(t1, t2) + 0.5 * (max(t1, t2) - min(t1, t2))

    def extract_target(self, step):
        if isinstance(step[_TARGET], dict):
            target = step[_TARGET]
        else:
            target = self.target.get(step[_TARGET])
        if not target:
            target_i, d = self.extract_target_diff(step[_TARGET])
            target = self.target.get(target_i)
        return target

    def extract_target_type(self, step) -> str:
        if isinstance(step, dict):
            return step.get(_TYPE, '')
        else:
            target, _ = self.extract_target_diff(step)
            return self.target[target].get(_TYPE, '')

    def extract_target_value(self, step, key) -> tuple[str, str | Any]:
        target_type: str = self.extract_target_type(step)
        if isinstance(step, dict):
            target = step
            d = 0
        else:
            target, d = self.extract_target_diff(step)
            target = self.target[target]

        if key in target:
            target_value = target[key]
        elif 'zone' in target:
            z = int(target['zone'])
            if target_type == 'heart.rate.zone':
                zones, *_ = self.hr_zones()
                t: dict[str, float] = {'min': zones[z], 'max': zones[z + 1]}
                target_value = str(t[key])
            elif target_type == 'power.zone':
                zones, *_ = Power.power_zones(self.rFTP, self.cFTP)
                t = {'min': zones[z - 1], 'max': zones[z]}
                target_value = str(t[key])
        else:
            target_value = str(0)

        if d != 0:
            target_value = str(self.target_variations(step, target_type, key))  # type: ignore
        return target_type, target_value

    @staticmethod
    def extract_target_diff(target: str) -> tuple[str, int]:
        if '>' in target:
            d, target_i = map(str.strip, target.split('>'))
            d = -int(d)
        elif '<' in target:
            d, target_i = map(str.strip, target.split('<'))
            d = int(d)
        else:
            target_i: str = target.strip()
            d = 0
        return target_i, d

    def _target_value(self, step_config, val, secondary=False) -> float:
        target_i: str = step_config.get(_SECONDARY) if secondary else step_config.get(_TARGET)
        return self._get_target_value(target_i, val)

    def target_variations(self, target: str, target_type: str, val: str) -> float:
        tv: float = 0.0
        target, d = self.extract_target_diff(target)
        if target_type == 'pace.zone':
            tv = round(
                self.time_difference_pace(self._get_target_value(target, key=val), d) / self.vVO2.to_pace(), 2)
        elif target_type == 'heart.rate.zone':
            s: float = self.convert_targetHR_to_targetvVO2(self.convert_HR_to_targetHR(
                self._get_target_value(target, key=val))) * self.vVO2.to_pace()
            s = self.time_difference_pace(s, d)
            tv = round(self.convert_targetvVO2_to_targetHR(s / self.vVO2.to_pace()), 2)
        return tv

    def _get_target_value(self, target, key) -> float:
        target_type, target_value = self.extract_target_value(target, key)
        if target_type == 'heart.rate.zone':
            return float(self.convert_targetHR_to_HR(float(target_value)))
        elif target_type == 'speed.zone':
            return float(target_value)
        elif target_type == 'pace.zone':
            if self.sport_type == 'running':
                return float(self.convert_targetPace_to_pace(float(target_value)))
            else:
                return float(target_value)
        else:
            return float(0)

    def _target_type(self, step_config, secondary=False) -> dict:
        target: str = step_config.get(_SECONDARY) if secondary else step_config.get(_TARGET)
        if isinstance(target, dict):
            return get_target_type(target[_TYPE])
        target, _ = self.extract_target_diff(target)
        if not target or (target not in self.target):
            return get_target_type('no.target')
        else:
            return get_target_type(self.target[target][_TYPE])

    def hr_zones(self) -> tuple[list[float], list[int], list[dict]]:
        zones: list[float] = [0.46, 0.6, 0.7, 0.8, self.convert_HR_to_targetHR(self.flt), 1.0, 1.1]
        hr_zones: list[int] = [self.convert_targetHR_to_HR(zone) for zone in zones]

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

    @staticmethod
    def convert_targetHR_to_targetvVO2(HR: float) -> float:
        return 0.9607 * HR + 0.0846  # HR + 0.06

    @staticmethod
    def convert_targetvVO2_to_targetHR(vVO2: float) -> float:
        return (vVO2 - 0.0846) / 0.9607  # vVO2 - 0.06

    @staticmethod
    def time_difference_pace(s: float, d: int) -> float:
        return 1000.0/(1000.0/s + d)

    def convert_targetHR_to_HR(self, target_value: float) -> int:
        return int(self.fmin + target_value * (self.fmax-self.fmin))

    def convert_HR_to_targetHR(self, HR: float) -> float:
        return (HR - self.fmin) / (self.fmax-self.fmin)

    def convert_HR_to_pace(self, HR) -> float:
        return self.convert_targetHR_to_targetvVO2(self.convert_HR_to_targetHR(HR)) * self.vVO2.to_pace()

    def convert_targetPace_to_pace(self, target_value: float) -> float:
        return target_value * self.vVO2.to_pace()

    def _generate_description(self) -> str | None:
        description: str = ''
        if self.sport_type == 'running':
            if self.plan == '' and _DESCRIPTION in self.config:
                description += self.config.get(_DESCRIPTION, '') + '. '
            if self.plan != '':
                description += 'Plan: ' + self.plan + '. '
            description += ('Estimated Duration: ' + str(self.duration) + '; '
                            + str(self.mileage).format('2:2f') + ' km. '
                            + str(timedelta(seconds=self.sec/self.mileage))[3:7]
                            + ' min/km - '
                            + str(round(self.ratio, 2)).format('2:2f') + '% vVO2. '
                            + 'rTSS: ' + str(self.tss).format('2:2f') + '. '
                            + 'ECOs: ' + str(round(self.ECOs, 2)).format('2:2f') + '. ')
        elif self.sport_type == 'cycling':
            description = 'FTP %d, TSS %d, NP %d, IF %.2f' % (
                float(self.cFTP.power[:-1]), self.tss, self.norm_pwr, self.int_fct)
        else:
            description = self.config.get(_DESCRIPTION, '') + '. '
            description += 'Plan: ' + self.plan + '. '
        if description:
            return description

    @staticmethod
    def extract_workout_id(workout) -> str:
        return workout.get(_WORKOUT_ID)

    @staticmethod
    def extract_workout_name(workout) -> str:
        return workout.get(_WORKOUT_NAME)

    @staticmethod
    def extract_workout_author(workout) -> dict:
        return workout.get('author')

    @staticmethod
    def extract_workout_description(workout) -> str:
        return workout.get(_DESCRIPTION)

    @staticmethod
    def extract_workout_owner_id(workout) -> str:
        return workout.get(_WORKOUT_OWNER_ID)

    @staticmethod
    def print_workout_json(workout) -> None:
        print(json.dumps(filter_empty(workout)))

    @staticmethod
    def print_workout_summary(workout) -> None:
        workout_id: str = Workout.extract_workout_id(workout)
        workout_name: str = Workout.extract_workout_name(workout)
        workout_description: str = Workout.extract_workout_description(workout)
        print('{0} {1:20} {2}'.format(workout_id, workout_name, workout_description))

    def get_estimated_duration(self) -> dict[str, float | None]:
        estimatedSec = None
        estimatedMet = None

        if self.sec > 0 and self.sport_type == 'running':
            estimatedSec: float | None = self.sec

        if self.mileage > 0 and self.sport_type == 'running':
            estimatedMet: float | None = self.mileage * 1000

        return {
            _ESTIMATED_DURATION: estimatedSec,
            _ESTIMATED_DISTANCE: estimatedMet,
            _AVG_SPEED: estimatedMet / estimatedSec if estimatedSec and estimatedMet else None,
        }

    def _steps(self, steps_config) -> list:
        steps, step_order, child_step_id, repeatDuration = self._steps_recursive(steps_config, 0, None)
        return steps

    def _steps_recursive(self, steps_config, step_order, child_step_id) -> tuple[list[Any], Any, Any, Any | None]:
        repeatDuration = None
        steps_config_agg = [(1, steps_config[0])]

        for step_config in steps_config[1:]:
            (repeats, prev_step_config) = steps_config_agg[-1]
            if prev_step_config == step_config:  # repeated step
                steps_config_agg[-1] = (repeats + 1, step_config)  # type: ignore
            else:
                steps_config_agg.append((1, step_config))

        steps: list = []
        for repeats, step_config in steps_config_agg:
            step_order = step_order + 1
            if isinstance(step_config, list):
                child_step_id = child_step_id + 1 if child_step_id else 1

                repeat_step_order = step_order
                repeat_child_step_id = child_step_id

                repeatDuration = step_config[0][_REPEAT_DURATION] if _REPEAT_DURATION in step_config[0] else None,
                repeatDuration = repeatDuration[0]

                nested_steps, step_order, child_step_id, amrat = self._steps_recursive(
                    step_config, step_order, child_step_id)
                steps.append(self._repeat_step(repeat_step_order, repeat_child_step_id, repeats, nested_steps,
                                               repeatDuration))
            else:
                steps.append(self._interval_step(step_config, child_step_id, step_order))

        return steps, step_order, child_step_id, repeatDuration

    def create_workout(self, workout_id=None, workout_owner_id=None, workout_author=None) -> dict:
        return {
            _WORKOUT_ID: workout_id,
            _WORKOUT_OWNER_ID: workout_owner_id,
            _WORKOUT_NAME: self.get_workout_name(),
            _DESCRIPTION: self._generate_description(),
            _WORKOUT_SPORT_TYPE: get_sport_type(self.sport_type),
            _WORKOUT_SUBSPORT_TYPE: self.subsport,
            _AUTHOR: workout_author,
            **self.get_estimated_duration(),
            _WORKOUT_SEGMENTS: [
                {
                    _WORKOUT_ORDER: 1,
                    _WORKOUT_SPORT_TYPE: get_sport_type(self.sport_type),
                    _WORKOUT_STEPS: self._steps(self.config.get(_STEPS))
                    }
                ],
            **get_pool('25m' if self.sport_type == 'swimming' else None),
            **get_estimate('DISTANCE_ESTIMATED' if self.sport_type == 'running' and self.mileage > 0 else None),
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
        return WorkoutStep(
            order=step_order,
            child_step_id=child_step_id,
            description=step_config.get(_DESCRIPTION) if _DESCRIPTION in step_config else None,
            step_type=step_config[_TYPE] if _TYPE in step_config else None,
            end_condition=WorkoutStep._end_condition(step_config)[_CONDITION_TYPE_KEY],
            end_condition_value=step_config[_DURATION] if _DURATION in step_config else None,
            category=step_config[_CATEGORY] if _CATEGORY in step_config else None,
            exerciseName=step_config[_EXERCISE_NAME] if _EXERCISE_NAME in step_config else None,
            target=Target(
                target=self._target_type(step_config)[_WORKOUT_TARGET_KEY],
                value_one=self._target_value(step_config, 'min'),
                value_two=self._target_value(step_config, 'max'),
                zone=self._target_value(step_config, 'zone') if 'zone' in step_config else None,
                secondary=False
            ),
            secondary_target=Target(
                target=self._target_type(step_config, _SECONDARY in step_config)[_WORKOUT_TARGET_KEY],
                value_one=self._target_value(step_config, 'min', _SECONDARY in step_config),
                value_two=self._target_value(step_config, 'max', _SECONDARY in step_config),
                zone=self._target_value(
                    step_config, 'zone', _SECONDARY in step_config) if 'zone' in step_config else None,
                secondary=True
            ) if _SECONDARY in step_config else None,
            weight=step_config[_WEIGHT] if _WEIGHT in step_config else None
        ).create_workout_step()
