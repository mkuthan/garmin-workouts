import logging
import yaml
import os
from garminworkouts.config.includeloader import IncludeLoader


def read_config(filename) -> dict:
    with open(filename, 'r') as f:
        data: dict = yaml.load(f, IncludeLoader)
        test_name: str = os.path.basename(filename).split('.')[0]
        s: str = data.get('name', '').split('-')[0].replace('D', '_').replace('W0', 'R').replace('W', 'R')

        if 'steps' in data:
            i = 0
            for step in data.get('steps', []):
                if len(step) == 1 and isinstance(step[0], list):
                    step: dict = step[0]
                data['steps'][i] = step
                i += 1

            if s not in test_name and 'goal' not in data:
                logging.warning(f"Name in config file '{s}' does not match filename '{test_name}'")
        else:
            if 'content' in data:
                if '-' in data['name']:
                    data['name'] = test_name + '-' + data.get('name', '').split('-')[1]
                else:
                    data['name'] = test_name + '-' + data.get('name', '')
    return data
