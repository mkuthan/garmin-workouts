import argparse
import pytest
from unittest.mock import patch
from garminworkouts.utils.validators import writeable_dir


def test_writeable_dir_valid():
    # Test with a valid writeable directory
    with patch('os.path.isdir', return_value=True), patch('os.access', return_value=True):
        assert writeable_dir('/path/to/writeable/dir') == '/path/to/writeable/dir'


def test_writeable_dir_not_a_directory():
    # Test with a path that is not a directory
    with patch('os.path.isdir', return_value=False):
        with pytest.raises(argparse.ArgumentTypeError) as excinfo:
            writeable_dir('/path/to/nonexistent/dir')
        assert "'/path/to/nonexistent/dir' is not a directory" in str(excinfo.value)


def test_writeable_dir_not_writeable():
    # Test with a directory that is not writeable
    with patch('os.path.isdir', return_value=True), patch('os.access', return_value=False):
        with pytest.raises(argparse.ArgumentTypeError) as excinfo:
            writeable_dir('/path/to/nonwriteable/dir')
        assert "'/path/to/nonwriteable/dir' is not a writeable directory" in str(excinfo.value)
