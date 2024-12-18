import os
import unittest

from garminworkouts.config import configreader
from unittest.mock import patch, mock_open


class MyTestCase(unittest.TestCase):
    def test_read_config(self) -> None:
        config_file: str = os.path.join(os.path.dirname(__file__), 'test_configreader.yaml')
        config: dict = configreader.read_config(config_file)

        expected_config: dict = {
            'name': 'Test',
            'steps':
                [
                    {'power': 50, 'duration': '2:00'},
                    [{'power': 90, 'duration': '12:00'},
                     {'power': 60, 'duration': '4:00'}],
                    [{'power': 90, 'duration': '12:00'},
                     {'power': 60, 'duration': '4:00'}],
                    {'power': 50, 'duration': '2:00'}
                ]
            }

        self.assertDictEqual(config, expected_config)

        config_file = os.path.join(os.path.dirname(__file__), 'test_configreader2.yaml')
        config: dict = configreader.read_config(config_file)

        expected_config: dict = {
            'name': 'Test',
            'steps':
                [[{'power': 90}, {'duration': '12:00'}]],
        }

        self.assertDictEqual(config, expected_config)

    class MyTestCase(unittest.TestCase):
        def setUp(self):
            self.config_file_path = os.path.join(os.path.dirname(__file__), 'test_configreader.yaml')
            self.config_file_path2 = os.path.join(os.path.dirname(__file__), 'test_configreader2.yaml')

        @patch("builtins.open", new_callable=mock_open, read_data="""
        name: Test-D
        steps:
          - power: 50
            duration: '2:00'
          - - power: 90
              duration: '12:00'
            - power: 60
              duration: '4:00'
          - - power: 90
              duration: '12:00'
            - power: 60
              duration: '4:00'
          - power: 50
            duration: '2:00'
        """)
        def test_read_config(self, mock_file):
            expected_config = {
                    'name': 'Test',
                    'steps': [
                        {'power': 50, 'duration': '2:00'},
                        {'power': 90, 'duration': '12:00'},
                        {'power': 60, 'duration': '4:00'},
                        {'power': 90, 'duration': '12:00'},
                        {'power': 60, 'duration': '4:00'},
                        {'power': 50, 'duration': '2:00'}
                    ]
                }

            config = configreader.read_config(self.config_file_path)
            self.assertDictEqual(config, expected_config)

        @patch("builtins.open", new_callable=mock_open, read_data="""
        name: Test-D
        steps:
          - - power: 90
              duration: '12:00'
        """)
        def test_read_config_with_nested_steps(self, mock_file):
            expected_config = {
                    'name': 'Test',
                    'steps': [
                        {'power': 90, 'duration': '12:00'}
                    ]
                }

            config = configreader.read_config(self.config_file_path2)
            self.assertDictEqual(config, expected_config)

        @patch("builtins.open", new_callable=mock_open, read_data="""
        name: Test-D
        content: some content
        """)
        def test_read_config_with_content(self, mock_file):
            expected_config = {
                    'name': 'test_configreader-Test',
                    'content': 'some content'
                }

            config = configreader.read_config(self.config_file_path)
            self.assertDictEqual(config, expected_config)

    if __name__ == '__main__':
        unittest.main()
