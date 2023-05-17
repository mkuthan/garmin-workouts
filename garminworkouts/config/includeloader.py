import os

import yaml


class IncludeLoader(yaml.SafeLoader):

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]  # type: ignore

        super(IncludeLoader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))  # type: ignore

        with open(filename, 'r') as f:
            d = yaml.load(f, IncludeLoader)

            if isinstance(d, list) and len(d) == 1:
                d = d[0]

        return d


IncludeLoader.add_constructor('!include', IncludeLoader.include)
