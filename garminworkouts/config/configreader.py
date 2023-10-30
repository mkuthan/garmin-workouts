import yaml

from garminworkouts.config.excelparser import excel_to_yaml
from garminworkouts.config.includeloader import IncludeLoader


def read_config(filename) -> dict:
    if "xls" in filename.split(".")[-1]:
        filename = excel_to_yaml(filename)

    with open(filename, 'r') as f:
        data: dict = yaml.load(f, IncludeLoader)
        if 'steps' in data and isinstance(data['steps'][0], list):
            data['steps'] = data['steps'][0]
    return data
