import os

import yaml
import garminworkouts.config.generator as generator
import datetime


@staticmethod
def extract_duration(s) -> str:
    if 'min' in s:
        duration = str(datetime.timedelta(minutes=float(s.split('min')[0])))
    elif 's' in s:
        duration = str(datetime.timedelta(seconds=float(s.split('s')[0])))
    elif ':' in s:
        duration = s
    elif 'km' in s:
        duration = s
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
def step_generator(s, duration, objective):
    step = s
    if '>' in step:
        step = step.split('>')[1]
    if '<' in step:
        step = step.split('<')[1]
    if '_' in step:
        step = step.split('_')[0]
    if 'p' in step[0]:
        step = step.split('p')[1]

    return generator_struct(s, duration, objective, step)


@staticmethod
def generator_struct(s, duration, objective, step) -> dict | list[dict]:
    match step:
        case 'recovery':
            d = generator.recovery_step_generator(duration, 'p' in s)
        case 'aerobic':
            d = generator.aerobic_step_generator(duration, 'p' in s)
        case 'lt':
            d = generator.lt_step_generator(s, duration, 'p' in s)
        case 'lr':
            d = generator.lr_step_generator(duration, 'p' in s)
        case 'marathon':
            d = generator.marathon_step_generator(s, duration, 'p' in s)
        case 'hm':
            d = generator.hm_step_generator(s, duration, 'p' in s)
        case 'tuneup':
            d = generator.tuneup_step_generator(duration)
        case 'warmup':
            d = generator.warmup_step_generator(duration)
        case 'cooldown':
            d = generator.cooldown_step_generator(duration, 'p' in s)
        case 'walk':
            d = generator.walk_step_generator(duration)
        case 'stride':
            d = generator.stride_generator(duration)
        case 'longhill':
            d = generator.longhill_generator(duration)
        case 'hill':
            d = generator.hill_generator(duration)
        case 'acceleration':
            d = generator.acceleration_generator(duration)
        case 'series':
            d = generator.series_generator(duration)
        case 'race':
            d = generator.race_generator(duration, objective)
        case _:
            d = {}

    return d


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

            d = step_generator(
                s[0],
                extract_duration(s[1]) if len(s) >= 2 else '',
                int(s[2].split('sub')[1]) if len(s) >= 3 else 0)

        if isinstance(d, list) and len(d) == 1:
            d = d[0]

        if len(d) == 0:
            print(filename + ' not found; empty step defined')

        return d


IncludeLoader.add_constructor('!include', IncludeLoader.include)
