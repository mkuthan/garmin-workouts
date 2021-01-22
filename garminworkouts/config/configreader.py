import yaml

from garminworkouts.config.includeloader import IncludeLoader
from garminworkouts.config.excelparser import excel_to_yaml


def read_config(filename,ftp):
    if "xls" in filename.split(".")[-1]:
        filename=excel_to_yaml(filename, ftp)

    with open(filename, 'r') as f:
        data = yaml.load(f, IncludeLoader)
    return data
