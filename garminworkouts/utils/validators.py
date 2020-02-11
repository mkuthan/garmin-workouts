import argparse
import os


def writeable_dir(directory):
    if not os.path.isdir(directory):
        raise argparse.ArgumentTypeError("'%s' is not a directory" % directory)
    if not os.access(directory, os.W_OK):
        raise argparse.ArgumentTypeError("'%s' is not a writeable directory" % directory)
    return directory
