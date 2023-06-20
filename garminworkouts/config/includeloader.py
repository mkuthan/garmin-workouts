import os

import yaml
import garminworkouts.config.generator as generator


@staticmethod
def extract_duration(s):
    if 'min' in s:
        duration = s.split('min')[0] + ':00'
    else:
        duration = s + 'km'
    return duration


@staticmethod
def step_generator(s, duration):
    d = {}

    if s == 'recovery':
        d = generator.recovery_step_generator(duration)
    elif s == 'aerobic':
        d = generator.aerobic_step_generator(duration)
    elif s == 'lt':
        d = generator.lt_step_generator(duration)
    elif s == 'lr':
        d = generator.lr_step_generator(duration)
    elif s == 'marathon':
        d = generator.marathon_step_generator(duration)
    elif s == 'hm':
        d = generator.hm_step_generator(duration)
    elif s == 'tuneup':
        d = generator.tuneup_step_generator(duration)
    elif s == 'cooldown':
        d = generator.cooldown_step_generator(duration)

    return d


class IncludeLoader(yaml.SafeLoader):

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]  # type: ignore

        super(IncludeLoader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))  # type: ignore

        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                d = yaml.load(f, IncludeLoader)
        else:
            s = os.path.split(filename)[-1]
            s = s.split('.')[0].split('_')

            d = step_generator(s[0], extract_duration(s[1]))

        if isinstance(d, list) and len(d) == 1:
            d = d[0]

        if len(d) == 0:
            print(filename + ' not found; empty step defined')

        return d


IncludeLoader.add_constructor('!include', IncludeLoader.include)
