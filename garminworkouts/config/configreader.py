import logging
import yaml
import os
from garminworkouts.config.includeloader import IncludeLoader


def read_config(filename) -> dict:
    with open(filename, 'r') as f:
        data: dict = yaml.load(f, IncludeLoader)
        if 'steps' in data:
            i = 0
            for step in data.get('steps', []):
                if len(step) == 1 and isinstance(step[0], list):
                    step: dict = step[0]
                data['steps'][i] = step
                i += 1
            test_name: str = os.path.basename(filename).split('.')[0]
            if not data['name'] in test_name:
                logging.warning(f"Name in config file '{data['name']}' does not match filename '{test_name}'")

    return data
