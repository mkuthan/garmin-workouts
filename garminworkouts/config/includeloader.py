import os
import re
import yaml
import garminworkouts.config.generators.running as running
import garminworkouts.config.generators.strength as strength
import datetime
import logging


@staticmethod
def extract_duration(s) -> str:
    if 'min' in s:
        return str(datetime.timedelta(minutes=float(s.split('min')[0])))
    elif 'reps' in s:
        return s.split('reps')[0]
    elif 's' in s:
        return str(datetime.timedelta(seconds=float(s.split('s')[0])))
    elif ':' in s:
        return s
    elif 'km' in s:
        return s
    elif 'mile' in s:
        return str(float(s.split('mile')[0])*1.609) + 'km'
    elif 'm' in s:
        return s
    elif 'k' in s:
        return s.split('k')[0] + 'km'
    elif 'half' in s:
        return '21.1km'
    else:
        return s.replace(',', '.') + 'km'


@staticmethod
def step_generator(s, duration, objective) -> dict | list[dict]:
    step = re.split(r'[><]', s)[-1]
    step = step.lstrip('p')
    return generator_struct(s, duration, objective, step)


@staticmethod
def generator_struct(name, duration, objective, step) -> dict | list[dict]:
    step_generators = {
        'R0': running.simple_step.R0_step_generator,
        'R1': running.simple_step.R1_step_generator,
        'R1p': running.simple_step.R1p_step_generator,
        'R2': lambda d: running.simple_step.R2_step_generator(d, name),
        'R3': lambda d: running.simple_step.R3_step_generator(d, name),
        'R3p': running.simple_step.R3p_step_generator,
        'R4': running.simple_step.R4_step_generator,
        'R5': running.simple_step.R5_step_generator,
        'R6': running.simple_step.R6_step_generator,
        'intervals': lambda d: running.multi_step.Rseries_generator(d, objective),
        'recovery': lambda d: running.simple_step.recovery_step_generator(d, 'p' in name),
        'aerobic': lambda d: running.simple_step.aerobic_step_generator(d, 'p' in name),
        'lt': lambda d: running.simple_step.lt_step_generator(d, name, 'p' in name),
        'lr': lambda d: running.simple_step.lr_step_generator(d, 'p' in name),
        'marathon': lambda d: running.simple_step.marathon_step_generator(d, name),
        'hm': lambda d: running.simple_step.hm_step_generator(d, name),
        'tuneup': running.simple_step.tuneup_step_generator,
        'warmup': running.simple_step.warmup_step_generator,
        'cooldown': lambda d: running.simple_step.cooldown_step_generator(d, 'p' in name),
        'walk': running.simple_step.walk_step_generator,
        'stride': running.multi_step.stride_generator,
        'longhill': running.multi_step.longhill_generator,
        'hill': running.multi_step.hill_generator,
        'acceleration': running.multi_step.acceleration_generator,
        'series': running.multi_step.series_generator,
        'anaerobic': running.multi_step.anaerobic_generator,
        'race': lambda d: running.multi_step.race_generator(d, objective),
        'PlankPushHold': strength.multi_step.plank_push_hold_generator,
        'PlankPushAngel': strength.multi_step.plank_push_angel_generator,
        'CalfHoldLunge': strength.multi_step.calf_hold_lunge_generator,
        'CalfLungeSide': strength.multi_step.calf_lunge_side_generator,
        'CalfLungeSquat': strength.multi_step.calf_lunge_squat_generator,
        'CalfSquatHold': strength.multi_step.calf_squat_hold_generator,
        'ClimberShouldertapPlankrot': strength.multi_step.climber_shoulder_tap_plank_rot_generator,
        'CalfHoldSquat': strength.multi_step.calf_hold_squat_generator,
        'LegRaiseHoldSitup': strength.multi_step.leg_raise_hold_situp_generator,
        'LegRaiseHoldSKneetwist': strength.multi_step.leg_raise_hold_kneetwist_generator,
        'MaxPushups': strength.multi_step.max_pushups_generator,
        'ShoulderTapUpdownPlankHold': strength.multi_step.shoulder_tap_updown_plank_hold_generator,
        'FlutterKickCrunch': strength.multi_step.flutter_kick_circle_high_crunch_generator,
        'PlankRotationWalkOutAltRaises': strength.multi_step.plank_rotation_walkout_altraises_generator,
    }

    generator = step_generators.get(step)
    if generator:
        return generator(duration)
    else:
        try:
            return getattr(strength.multi_step, camel_to_snake(step) + '_generator')(duration)
        except AttributeError:
            return {}


def camel_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


class IncludeLoader(yaml.SafeLoader):

    def __init__(self, stream) -> None:
        self._root = os.path.split(stream.name)[0]  # type: ignore

        super(IncludeLoader, self).__init__(stream)

    def include(self, node):
        filename: str = os.path.join(self._root, self.construct_scalar(node))  # type: ignore

        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                d = yaml.load(f, IncludeLoader)
        else:
            d = self.generate_step_from_filename(filename)

        if isinstance(d, list) and len(d) == 1:
            d = d[0]

        if not d:
            logging.error(f"{filename} not found; empty step defined")

        return d

    def generate_step_from_filename(self, filename):
        try:
            s = os.path.split(filename)[-1].split('.')[0].split('_')
            name = s[0]
            duration = extract_duration(s[1]) if len(s) >= 2 else ''

            if 'intervals' in name:
                duration = [extract_duration(s[1]), extract_duration(s[2])]
                s = name.split('-')
                name = s[0]
                objective = [s[1], s[2]]
            else:
                objective = int(s[2].split('sub')[1]) if len(s) >= 3 else 0

            return step_generator(name, duration, objective)
        except (ValueError, IndexError):
            return []


IncludeLoader.add_constructor('!include', IncludeLoader.include)
