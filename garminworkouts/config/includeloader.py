import os
import yaml
import garminworkouts.config.generators.running as running
import garminworkouts.config.generators.strength as strength
import datetime


@staticmethod
def extract_duration(s) -> str:
    if 'min' in s:
        duration = str(datetime.timedelta(minutes=float(s.split('min')[0])))
    elif 'reps' in s:
        duration = s.split('reps')[0]
    elif 's' in s:
        duration = str(datetime.timedelta(seconds=float(s.split('s')[0])))
    elif ':' in s:
        duration: str = s
    elif 'km' in s:
        duration = s
    elif 'mile' in s:
        duration = str(float(s.split('mile')[0])*1.609) + 'km'
    elif 'm' in s:
        duration = s
    elif 'k' in s:
        duration = s.split('k')[0] + 'km'
    elif 'half' in s:
        duration = '21.1km'
    else:
        duration = s.replace(',', '.') + 'km'
    return duration


@staticmethod
def step_generator(s, duration, objective) -> dict | list[dict]:
    step: str = s
    if '>' in step:
        step = step.split('>')[1]
    if '<' in step:
        step = step.split('<')[1]
    if 'p' in step[0]:
        step = step.split('p')[1]

    return generator_struct(s, duration, objective, step)


@staticmethod
def generator_struct(s, duration, objective, step) -> dict | list[dict]:
    match step:
        case 'recovery':
            return running.simple_step.recovery_step_generator(duration, 'p' in s)
        case 'aerobic':
            return running.simple_step.aerobic_step_generator(duration, 'p' in s)
        case 'lt':
            return running.simple_step.lt_step_generator(s, duration, 'p' in s)
        case 'lr':
            return running.simple_step.lr_step_generator(duration, 'p' in s)
        case 'marathon':
            return running.simple_step.marathon_step_generator(s, duration, 'p' in s)
        case 'hm':
            return running.simple_step.hm_step_generator(s, duration, 'p' in s)
        case 'tuneup':
            return running.simple_step.tuneup_step_generator(duration)
        case 'warmup':
            return running.simple_step.warmup_step_generator(duration)
        case 'cooldown':
            return running.simple_step.cooldown_step_generator(duration, 'p' in s)
        case 'walk':
            return running.simple_step.walk_step_generator(duration)
        case 'stride':
            return running.multi_step.stride_generator(duration)
        case 'longhill':
            return running.multi_step.longhill_generator(duration)
        case 'hill':
            return running.multi_step.hill_generator()
        case 'acceleration':
            return running.multi_step.acceleration_generator()
        case 'series':
            return running.multi_step.series_generator(duration)
        case 'anaerobic':
            return running.multi_step.anaerobic_generator(duration)
        case 'race':
            return running.multi_step.race_generator(duration, objective)
        case 'PlankPushHold':
            return strength.multi_step.plank_push_hold_generator(duration)
        case 'PlankPushAngel':
            return strength.multi_step.plank_push_angel_generator(duration)
        case 'CalfHoldLunge':
            return strength.multi_step.calf_hold_lunge_generator(duration)
        case 'CalfLungeSide':
            return strength.multi_step.calf_lunge_side_generator(duration)
        case 'CalfLungeSquat':
            return strength.multi_step.calf_lunge_squat_generator(duration)
        case 'CalfSquatHold':
            return strength.multi_step.calf_squat_hold_generator(duration)
        case 'ClimberShouldertapPlankrot':
            return strength.multi_step.climber_shoulder_tap_plank_rot_generator(duration)
        case 'CalfHoldSquat':
            return strength.multi_step.calf_hold_squat_generator(duration)
        case 'LegRaiseHoldSitup':
            return strength.multi_step.leg_raise_hold_situp(duration)
        case 'LegRaiseHoldSKneetwist':
            return strength.multi_step.leg_raise_hold_kneetwist(duration)
        case 'MaxPushups':
            return strength.multi_step.max_pushups()
        case 'ShoulderTapUpdownPlankHold':
            return strength.multi_step.shoulder_tap_updown_plank_hold(duration)
        case 'FlutterKickCrunch':
            return strength.multi_step.flutter_kick_circle_high_crunch(duration)
        case 'PlankRotationWalkOutAltRaises':
            return strength.multi_step.plank_rotation_walkout_altraises(duration)
        case _:
            return {}


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
            s = os.path.split(filename)[-1]
            s = s.split('.')[0].split('_')

            try:
                d = step_generator(
                    s[0],
                    extract_duration(s[1]) if len(s) >= 2 else '',
                    int(s[2].split('sub')[1]) if len(s) >= 3 else 0)
            except ValueError:
                print(filename)
                d = step_generator(
                    s[0],
                    extract_duration(s[1]) if len(s) >= 2 else '',
                    0)
            except IndexError:
                print(filename)
                d = step_generator(
                    s[0],
                    extract_duration(s[1]) if len(s) >= 2 else '',
                    0)

        if isinstance(d, list) and len(d) == 1:
            d = d[0]

        if len(d) == 0:
            print(filename + ' not found; empty step defined')

        return d


IncludeLoader.add_constructor('!include', IncludeLoader.include)
