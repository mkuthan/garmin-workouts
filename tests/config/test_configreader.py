import os
import unittest

from garminworkouts.config import configreader


class MyTestCase(unittest.TestCase):
    def test_read_config(self) -> None:
        config_file = os.path.join(os.path.dirname(__file__), 'test_configreader.yaml')
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


if __name__ == '__main__':
    unittest.main()
