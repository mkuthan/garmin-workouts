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
            steps = []
            for step in data.get('steps', []):
                if isinstance(step, list) and isinstance(step[0], list):
                    for u in step[0]:
                        if isinstance(u, list):
                            u = u[0]
                            steps.append(u)
                        else:
                            steps.append(u)
                else:
                    steps.append(step)
            data['steps'] = steps
            if s not in test_name and 'goal' not in data:
                logging.warning(f"Name in config file '{s}' does not match filename '{test_name}'")
        else:
            if 'content' in data:
                if '-' in data['name']:
                    data['name'] = test_name + '-' + data.get('name', '').split('-')[1]
                else:
                    data['name'] = test_name + '-' + data.get('name', '')
    return data
