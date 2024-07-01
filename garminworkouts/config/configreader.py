import yaml

from garminworkouts.config.includeloader import IncludeLoader


def read_config(filename) -> dict:
    with open(filename, 'r') as f:
        data: dict = yaml.load(f, IncludeLoader)
        if 'steps' in data:
            i = 0
            for step in data.get('steps', []):
                if len(step) == 1 and isinstance(step[0], list):
                    step = step[0]
                data['steps'][i] = step
                i += 1
    return data
