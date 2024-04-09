import os
import unittest

from garminworkouts.config import configreader
from garminworkouts.config import generator
from garminworkouts.config import includeloader


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
                            'target': 'THRESHOLD_HEART_RATE',
                            'description': 'Threshold pace'
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
                            'target': 'MARATHON_HEART_RATE',
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
                        {
                            'type': 'warmup',
                            'duration': '1km',
                            'target': 'AEROBIC_HEART_RATE',
                            'description': 'Warm up'
                        },
                        {
                            'type': 'cooldown',
                            'duration': '1km',
                            'target': 'AEROBIC_HEART_RATE',
                            'description': 'Cool down'
                        },
                        {
                            'type': 'rest',
                            'duration': '1km',
                            'target': 'WALK',
                            'description': 'Walk'
                        },
                        [{
                            'type': 'interval',
                            'duration': '100m',
                            'target': '1KM_PACE',
                            'description': 'Strides pace'
                        },
                         {
                            'type': 'rest',
                            'duration': '100m',
                            'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace'
                        }],
                        [{
                            'type': 'interval', 'duration': '100m', 'target': '5KM_PACE',
                            'description': 'Long hill climbing'
                            },
                         {
                            'type': 'rest',
                            'duration': '200m',
                            'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace'
                            }],
                        [{
                            'type': 'interval', 'duration': '0:10', 'target': '1KM_PACE', 'description': 'Hill climbing'
                         },
                         {
                            'type': 'rest',
                            'duration': '0:20',
                            'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace'
                        }],
                        [{
                            'type': 'interval',
                            'duration': '0:30',
                            'target': '1KM_PACE',
                            'description': 'Accelerations'
                         },
                         {
                            'type': 'rest', 'duration': '0:30', 'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace'
                        }],
                        [{
                            'type': 'interval', 'duration': '1km', 'target': '5KM_PACE',
                            'description': 'Series @5k pace'
                         },
                         {
                            'type': 'rest', 'duration': '2:30', 'target': 'RECOVERY_PACE', 'description': 'Recovery'
                            }],
                        [{
                            'type': 'interval', 'duration': '1000m', 'target': '1500M_PACE',
                            'description': 'Series @1500 pace'
                        },
                         {
                            'type': 'rest', 'duration': '1:00', 'target': 'WALK', 'description': 'Recovery pace'
                        }],
                        {
                            'type': 'interval', 'duration': '5km',
                            'target': 'HEART_RATE_ZONE_4', 'description': '5k race'
                        },
                        {},
                        {
                            'type': 'interval', 'duration': '5km',
                            'target': 'HEART_RATE_ZONE_4', 'description': '5k race'
                        },
            ]
        }

        self.assertDictEqual(config, expected_config)

    def test_race_steps_generator(self) -> None:
        self.assertEqual(generator.race_steps_generator(z1='5km', description=''),
                         [{'type': 'interval', 'duration': '5km', 'target': 'HEART_RATE_ZONE_1', 'description': ''}])
        self.assertEqual(generator.race_steps_generator(z2='5km', description=''),
                         [{'type': 'interval', 'duration': '5km', 'target': 'HEART_RATE_ZONE_2', 'description': ''}])
        self.assertEqual(generator.race_steps_generator(z3='5km', description=''),
                         [{'type': 'interval', 'duration': '5km', 'target': 'HEART_RATE_ZONE_3', 'description': ''}])
        self.assertEqual(generator.race_steps_generator(z4='5km', description=''),
                         [{'type': 'interval', 'duration': '5km', 'target': 'HEART_RATE_ZONE_4', 'description': ''}])

    def test_race_generator(self) -> None:
        self.assertEqual(generator.race_generator('5km', 20),
                         generator.race_steps_generator(z4='5km', description='5k race'))
        self.assertEqual(generator.race_generator('5km', 25),
                         generator.race_steps_generator(z3='1km', z4='4km', description='5k race'))
        self.assertEqual(generator.race_generator('5km', 30),
                         generator.race_steps_generator(z3='2km', z4='3km', description='5k race'))
        self.assertEqual(generator.race_generator('5km', 40),
                         generator.race_steps_generator(z3='3km', z4='2km', description='5k race'))
        self.assertEqual(generator.race_generator('6km', 20),
                         generator.race_steps_generator(z4='6km', description='6k race'))
        self.assertEqual(generator.race_generator('6km', 25),
                         generator.race_steps_generator(z3='1km', z4='5km', description='6k race'))
        self.assertEqual(generator.race_generator('6km', 30),
                         generator.race_steps_generator(z3='2km', z4='4km', description='6k race'))
        self.assertEqual(generator.race_generator('6km', 36),
                         generator.race_steps_generator(z3='3km', z4='3km', description='6k race'))
        self.assertEqual(generator.race_generator('6km', 40),
                         generator.race_steps_generator(z3='4km', z4='2km', description='6k race'))
        self.assertEqual(generator.race_generator('10km', 30),
                         generator.race_steps_generator(z3='4km', z4='6km', description='10k race'))
        self.assertEqual(generator.race_generator('10km', 40),
                         generator.race_steps_generator(z3='5km', z4='5km', description='10k race'))
        self.assertEqual(generator.race_generator('10km', 50),
                         generator.race_steps_generator(z3='6km', z4='4km', description='10k race'))
        self.assertEqual(generator.race_generator('10km', 60),
                         generator.race_steps_generator(z3='7km', z4='3km', description='10k race'))
        self.assertEqual(generator.race_generator('10km', 70),
                         generator.race_steps_generator(z3='8km', z4='2km', description='10k race'))
        self.assertEqual(generator.race_generator('15km', 60),
                         generator.race_steps_generator(z3='10km', z4='5km', description='15k race'))
        self.assertEqual(generator.race_generator('15km', 75),
                         generator.race_steps_generator(z3='11km', z4='4km', description='15k race'))
        self.assertEqual(generator.race_generator('15km', 90),
                         generator.race_steps_generator(z3='12km', z4='3km', description='15k race'))
        self.assertEqual(generator.race_generator('15km', 100),
                         generator.race_steps_generator(z3='13km', z4='2km', description='15k race'))
        self.assertEqual(generator.race_generator('20km', 70),
                         generator.race_steps_generator(z2='7km', z3='11km', z4='2km', description='20k race'))
        self.assertEqual(generator.race_generator('20km', 80),
                         generator.race_steps_generator(z2='8km', z3='10km', z4='2km', description='20k race'))
        self.assertEqual(generator.race_generator('20km', 90),
                         generator.race_steps_generator(z2='9km', z3='9km', z4='2km', description='20k race'))
        self.assertEqual(generator.race_generator('20km', 100),
                         generator.race_steps_generator(z2='10km', z3='8km', z4='2km', description='20k race'))
        self.assertEqual(generator.race_generator('20km', 110),
                         generator.race_steps_generator(z2='11km', z3='7km', z4='2km', description='20k race'))
        self.assertEqual(generator.race_generator('20km', 120),
                         generator.race_steps_generator(z2='12km', z3='6km', z4='2km', description='20k race'))
        self.assertEqual(generator.race_generator('20km', 130),
                         generator.race_steps_generator(z2='13km', z3='5km', z4='2km', description='20k race'))
        self.assertEqual(generator.race_generator('21.1km', 80),
                         generator.race_steps_generator(z2='8km', z3='11km', z4='2.1km',
                                                        description='Half marathon race'))
        self.assertEqual(generator.race_generator('21.1km', 90),
                         generator.race_steps_generator(z2='9km', z3='10km', z4='2.1km',
                                                        description='Half marathon race'))
        self.assertEqual(generator.race_generator('21.1km', 100),
                         generator.race_steps_generator(z2='10km', z3='9km', z4='2.1km',
                                                        description='Half marathon race'))
        self.assertEqual(generator.race_generator('21.1km', 110),
                         generator.race_steps_generator(z2='11km', z3='8km', z4='2.1km',
                                                        description='Half marathon race'))
        self.assertEqual(generator.race_generator('21.1km', 120),
                         generator.race_steps_generator(z2='12km', z3='7km', z4='2.1km',
                                                        description='Half marathon race'))
        self.assertEqual(generator.race_generator('21.1km', 130),
                         generator.race_steps_generator(z2='13km', z3='6km', z4='2.1km',
                                                        description='Half marathon race'))
        self.assertEqual(generator.race_generator('21.1km', 140),
                         generator.race_steps_generator(z2='14km', z3='5km', z4='2.1km',
                                                        description='Half marathon race'))
        self.assertEqual(generator.race_generator('marathon', 150),
                         generator.race_steps_generator(z1='3km', z2='25km', z3='14.2km', description='Marathon race'))
        self.assertEqual(generator.race_generator('marathon', 195),
                         generator.race_steps_generator(z1='7km', z2='25km', z3='10.2km', description='Marathon race'))
        self.assertEqual(generator.race_generator('marathon', 220),
                         generator.race_steps_generator(z1='10km', z2='25km', z3='7.2km', description='Marathon race'))
        self.assertEqual(generator.race_generator('marathon', 240),
                         generator.race_steps_generator(z1='12km', z2='25km', z3='5.2km', description='Marathon race'))
        self.assertEqual(generator.race_generator('marathon', 250),
                         generator.race_steps_generator(z1='15km', z2='25km', z3='2.2km', description='Marathon race'))

    def test_extract_duration(self) -> None:
        self.assertEqual(includeloader.extract_duration('1min'), '0:01:00')
        self.assertEqual(includeloader.extract_duration('30s'), '0:00:30')
        self.assertEqual(includeloader.extract_duration('1:00'), '1:00')
        self.assertEqual(includeloader.extract_duration('1km'), '1km')
        self.assertEqual(includeloader.extract_duration('1000m'), '1000m')
        self.assertEqual(includeloader.extract_duration('1k'), '1km')
        self.assertEqual(includeloader.extract_duration('half'), '21.1km')
        self.assertEqual(includeloader.extract_duration('1,5'), '1.5km')


if __name__ == '__main__':
    unittest.main()
