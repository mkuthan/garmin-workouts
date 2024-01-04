import yaml

from garminworkouts.config.includeloader import IncludeLoader


def read_config(filename) -> dict:
    with open(filename, 'r') as f:
        data: dict = yaml.load(f, IncludeLoader)
        if 'steps' in data and len(data['steps']) == 1 and isinstance(data['steps'][0], list):
            data['steps'] = data['steps'][0]
    return data
