import argparse
import os
from typing import Any


def writeable_dir(directory) -> Any:
    if not os.path.isdir(directory):
        raise argparse.ArgumentTypeError("'%s' is not a directory" % directory)
    if not os.access(directory, os.W_OK):
        raise argparse.ArgumentTypeError("'%s' is not a writeable directory" % directory)
    return directory
