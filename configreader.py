import os

import yaml


class ConfigReader(object):

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, 'r') as f:
            data = yaml.load(f, IncludeLoader)
        return data


class IncludeLoader(yaml.SafeLoader):

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]

        super(IncludeLoader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, IncludeLoader)


IncludeLoader.add_constructor('!include', IncludeLoader.include)
