import argparse
import os


def writeable_dir(directory):
    if not os.path.isdir(directory):
        raise argparse.ArgumentTypeError(f"'{directory}' is not a directory")
    if not os.access(directory, os.W_OK):
        raise argparse.ArgumentTypeError(f"'{directory}' is not a writeable directory")
    return directory
