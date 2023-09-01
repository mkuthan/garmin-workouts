import os
import unittest

from garminworkouts.config import configreader


class MyTestCase(unittest.TestCase):
    def test_read_generator(self) -> None:
        config_file = os.path.join(os.path.dirname(__file__), 'test_generator.yaml')
        config: dict = configreader.read_config(config_file)

        expected_config: dict = {
            'name': 'Test',
            'steps': [
                        {
                            'type': 'recovery',
                            'duration': '1km',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace'
                        },
                        {
                            'type': 'recovery',
                            'duration': '1.5km',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace'
                        },
                        {
                            'type': 'recovery',
                            'duration': '0:01:00',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace'
                        },
                        {
                            'type': 'recovery',
                            'duration': '1:20:00',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace'
                        },
                        {
                            'type': 'recovery',
                            'duration': '0:00:50',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace'
                        },
                        {
                            'type': 'recovery',
                            'duration': '0:01:30',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace'
                        },
                        {
                            'type': 'recovery',
                            'duration': '1km',
                            'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '1km',
                            'target': 'AEROBIC_PACE',
                            'description': 'Aerobic pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '5km',
                            'target': 'AEROBIC_HEART_RATE',
                            'description': 'Aerobic pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': 'THRESHOLD_PACE',
                            'description': 'Threshold pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': '10<THRESHOLD_PACE',
                            'description': '10s slower than Threshold pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': '10>THRESHOLD_PACE',
                            'description': '10s quicker than Threshold pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '1km',
                            'target': 'LONG_RUN_PACE',
                            'description': 'Long run pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '5km',
                            'target': 'LONG_RUN_HEART_RATE',
                            'description': 'Long run pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': 'MARATHON_PACE',
                            'description': 'Marathon pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': '10<MARATHON_PACE',
                            'description': '10s slower than Marathon pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': '10>MARATHON_PACE',
                            'description': '10s quicker than Marathon pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': 'HALF_MARATHON_PACE',
                            'description': 'Half Marathon pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': '10<HALF_MARATHON_PACE',
                            'description': '10s slower than Half Marathon pace'
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': '10>HALF_MARATHON_PACE',
                            'description': '10s quicker than Half Marathon pace'
                        },
            ]
        }

        self.assertDictEqual(config, expected_config)


if __name__ == '__main__':
    unittest.main()
