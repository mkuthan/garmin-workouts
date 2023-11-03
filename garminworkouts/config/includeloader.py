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
    else:
        duration = s.replace(',', '.') + 'km'
    return duration


@staticmethod
def step_generator(s, duration):
    step = s
    if '>' in step:
        step = step.split('>')[1]
    if '<' in step:
        step = step.split('<')[1]
    if '_' in step:
        step = step.split('_')[0]
    if 'p' in step[0]:
        step = step.split('p')[1]

    return generator_struct(s, duration)[step]


@staticmethod
def generator_struct(s, duration):
    d = {
        'recovery': generator.recovery_step_generator(duration, 'p' in s),
        'aerobic': generator.aerobic_step_generator(duration, 'p' in s),
        'lt': generator.lt_step_generator(s, duration, 'p' in s),
        'lr': generator.lr_step_generator(duration, 'p' in s),
        'marathon': generator.marathon_step_generator(s, duration, 'p' in s),
        'hm': generator.hm_step_generator(s, duration, 'p' in s),
        'tuneup': generator.tuneup_step_generator(duration),
        'warmup': generator.cooldown_step_generator(duration),
        'cooldown': generator.cooldown_step_generator(duration, 'p' in s),
        'walk': generator.walk_step_generator(duration),
        'stride': generator.stride_generator(duration),
        'hill': generator.hill_generator(duration),
    }
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

            d = step_generator(s[0], extract_duration(s[1]) if len(s) >= 2 else '')

        if isinstance(d, list) and len(d) == 1:
            d = d[0]

        if len(d) == 0:
            print(filename + ' not found; empty step defined')

        return d


IncludeLoader.add_constructor('!include', IncludeLoader.include)
