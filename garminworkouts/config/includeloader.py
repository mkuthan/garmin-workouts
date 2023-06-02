import os

import yaml
import garminworkouts.config.generator as generator


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

            d = {}
            duration = s[1] + 'km'

            if s[0] == 'recovery':
                d = generator.recovery_step_generator(duration)
            elif s[0] == 'aerobic':
                d = generator.aerobic_step_generator(duration)
            elif s[0] == 'lt':
                d = generator.lt_step_generator(duration)
            elif s[0] == 'lr':
                d = generator.lr_step_generator(duration)
            elif s[0] == 'marathon':
                d = generator.marathon_step_generator(duration)
            elif s[0] == 'hm':
                d = generator.hm_step_generator(duration)
            elif s[0] == 'cooldown':
                d = generator.cooldown_step_generator(duration)

        if isinstance(d, list) and len(d) == 1:
            d = d[0]

        return d


IncludeLoader.add_constructor('!include', IncludeLoader.include)
