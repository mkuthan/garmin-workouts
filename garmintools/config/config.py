import yaml

from config.includeloader import IncludeLoader


def read_config(filename):
    with open(filename, 'r') as f:
        data = yaml.load(f, IncludeLoader)
    return data
