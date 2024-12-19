import os
import unittest

from garminworkouts.config import configreader
from garminworkouts.config import includeloader
from garminworkouts.config.generators import running, strength
from garminworkouts.config.generators.strength.simple_step import exercise_generator


class MyTestCase(unittest.TestCase):
    def test_read_generator(self) -> None:
        config_file: str = os.path.join(os.path.dirname(__file__), 'test_generator.yaml')
        config: dict = configreader.read_config(config_file)

        expected_config: dict = {
            'name': 'Test',
            'steps': [
                        {
                            'type': 'recovery',
                            'duration': '1km',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'recovery',
                            'duration': '1.5km',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'recovery',
                            'duration': '0:01:00',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'recovery',
                            'duration': '1:20:00',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'recovery',
                            'duration': '0:00:50',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'recovery',
                            'duration': '0:01:30',
                            'target': 'RECOVERY_HEART_RATE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'recovery',
                            'duration': '1km',
                            'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '1km',
                            'target': 'AEROBIC_PACE',
                            'description': 'Aerobic pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '5km',
                            'target': 'AEROBIC_HEART_RATE',
                            'description': 'Aerobic pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': 'THRESHOLD_HEART_RATE',
                            'description': 'Threshold pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': 'THRESHOLD_PACE',
                            'description': 'Threshold pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': '10<THRESHOLD_PACE',
                            'description': '10s slower than Threshold pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': '10>THRESHOLD_PACE',
                            'description': '10s quicker than Threshold pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '1km',
                            'target': 'LONG_RUN_PACE',
                            'description': 'Long run pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '5km',
                            'target': 'LONG_RUN_HEART_RATE',
                            'description': 'Long run pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': 'MARATHON_PACE',
                            'description': 'Marathon pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': 'HALF_MARATHON_PACE',
                            'description': 'Half Marathon pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': '10<HALF_MARATHON_PACE',
                            'description': '10s slower than Half Marathon pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'interval',
                            'duration': '0:20:00',
                            'target': '10>HALF_MARATHON_PACE',
                            'description': '10s quicker than Half Marathon pace',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'warmup',
                            'duration': '1km',
                            'target': 'AEROBIC_HEART_RATE',
                            'description': 'Warm up',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'cooldown',
                            'duration': '1km',
                            'target': 'AEROBIC_HEART_RATE',
                            'description': 'Cool down',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'rest',
                            'duration': '1km',
                            'target': 'WALK',
                            'description': 'Walk',
                            'category': None,
                            'exerciseName': None,
                        },
                        [{
                            'type': 'interval',
                            'duration': '100m',
                            'target': '1KM_PACE',
                            'description': 'Strides pace',
                            'category': None,
                            'exerciseName': None,
                        },
                         {
                            'type': 'rest',
                            'duration': '100m',
                            'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        }],
                        [{
                            'type': 'interval', 'duration': '100m', 'target': '5KM_PACE',
                            'description': 'Long hill climbing',
                            'category': None,
                            'exerciseName': None,
                            },
                         {
                            'type': 'rest',
                            'duration': '200m',
                            'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                            }],
                        [{
                            'type': 'interval', 'duration': '0:10', 'target': '1KM_PACE',
                            'description': 'Hill climbing',
                            'category': None,
                            'exerciseName': None,
                         },
                         {
                            'type': 'rest',
                            'duration': '0:20',
                            'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        }],
                        [{
                            'type': 'interval',
                            'duration': '0:30',
                            'target': '1KM_PACE',
                            'description': 'Accelerations',
                            'category': None,
                            'exerciseName': None,
                         },
                         {
                            'type': 'rest', 'duration': '0:30', 'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        }],
                        [{
                            'type': 'interval', 'duration': '1km', 'target': '5KM_PACE',
                            'description': 'Series @5k pace',
                            'category': None,
                            'exerciseName': None,
                         },
                         {
                            'type': 'rest', 'duration': '2:30', 'target': 'RECOVERY_PACE', 'description': 'Recovery',
                            'category': None,
                            'exerciseName': None,
                            }],
                        [{
                            'type': 'interval', 'duration': '1000m', 'target': '1500M_PACE',
                            'description': 'Series @1500 pace',
                            'category': None,
                            'exerciseName': None,
                        },
                         {
                            'type': 'rest', 'duration': '1:00', 'target': 'RECOVERY_PACE',
                            'description': 'Recovery pace',
                            'category': None,
                            'exerciseName': None,
                        }],
                        {
                            'type': 'interval', 'duration': '5km',
                            'target': 'HEART_RATE_ZONE_4', 'description': '5k race',
                            'category': None,
                            'exerciseName': None,
                        },
                        {
                            'type': 'rest',
                            'duration': '1km',
                            'target': 'WALK',
                            'description': 'Walk',
                            'category': None,
                            'exerciseName': None,
                        },
            ]
        }

        self.assertDictEqual(config, expected_config)

    def test_race_steps_generator(self) -> None:
        self.assertEqual(running.multi_step.race_steps_generator(z1='5km', description=''),
                         [{'type': 'interval', 'duration': '5km', 'target': 'HEART_RATE_ZONE_1', 'description': '',
                          'category': None, 'exerciseName': None}])
        self.assertEqual(running.multi_step.race_steps_generator(z2='5km', description=''),
                         [{'type': 'interval', 'duration': '5km', 'target': 'HEART_RATE_ZONE_2', 'description': '',
                          'category': None, 'exerciseName': None}])
        self.assertEqual(running.multi_step.race_steps_generator(z3='5km', description=''),
                         [{'type': 'interval', 'duration': '5km', 'target': 'HEART_RATE_ZONE_3', 'description': '',
                          'category': None, 'exerciseName': None}])
        self.assertEqual(running.multi_step.race_steps_generator(z4='5km', description=''),
                         [{'type': 'interval', 'duration': '5km', 'target': 'HEART_RATE_ZONE_4', 'description': '',
                          'category': None, 'exerciseName': None}])

    def test_race_generator(self) -> None:
        self.assertEqual(running.multi_step.race_generator('5km', 20),
                         running.multi_step.race_steps_generator(z4='5km', description='5k race'))
        self.assertEqual(running.multi_step.race_generator('5km', 25),
                         running.multi_step.race_steps_generator(z3='1km', z4='4km', description='5k race'))
        self.assertEqual(running.multi_step.race_generator('5km', 30),
                         running.multi_step.race_steps_generator(z3='2km', z4='3km', description='5k race'))
        self.assertEqual(running.multi_step.race_generator('5km', 40),
                         running.multi_step.race_steps_generator(z3='3km', z4='2km', description='5k race'))
        self.assertEqual(running.multi_step.race_generator('6km', 20),
                         running.multi_step.race_steps_generator(z4='6km', description='6k race'))
        self.assertEqual(running.multi_step.race_generator('6km', 25),
                         running.multi_step.race_steps_generator(z3='1km', z4='5km', description='6k race'))
        self.assertEqual(running.multi_step.race_generator('6km', 30),
                         running.multi_step.race_steps_generator(z3='2km', z4='4km', description='6k race'))
        self.assertEqual(running.multi_step.race_generator('6km', 36),
                         running.multi_step.race_steps_generator(z3='3km', z4='3km', description='6k race'))
        self.assertEqual(running.multi_step.race_generator('6km', 40),
                         running.multi_step.race_steps_generator(z3='4km', z4='2km', description='6k race'))
        self.assertEqual(running.multi_step.race_generator('10km', 30),
                         running.multi_step.race_steps_generator(z3='4km', z4='6km', description='10k race'))
        self.assertEqual(running.multi_step.race_generator('10km', 40),
                         running.multi_step.race_steps_generator(z3='5km', z4='5km', description='10k race'))
        self.assertEqual(running.multi_step.race_generator('10km', 50),
                         running.multi_step.race_steps_generator(z3='6km', z4='4km', description='10k race'))
        self.assertEqual(running.multi_step.race_generator('10km', 60),
                         running.multi_step.race_steps_generator(z3='7km', z4='3km', description='10k race'))
        self.assertEqual(running.multi_step.race_generator('10km', 70),
                         running.multi_step.race_steps_generator(z3='8km', z4='2km', description='10k race'))
        self.assertEqual(running.multi_step.race_generator('15km', 60),
                         running.multi_step.race_steps_generator(z3='10km', z4='5km', description='15k race'))
        self.assertEqual(running.multi_step.race_generator('15km', 75),
                         running.multi_step.race_steps_generator(z3='11km', z4='4km', description='15k race'))
        self.assertEqual(running.multi_step.race_generator('15km', 90),
                         running.multi_step.race_steps_generator(z3='12km', z4='3km', description='15k race'))
        self.assertEqual(running.multi_step.race_generator('15km', 100),
                         running.multi_step.race_steps_generator(z3='13km', z4='2km', description='15k race'))
        self.assertEqual(running.multi_step.race_generator('20km', 70),
                         running.multi_step.race_steps_generator(z2='7km', z3='11km', z4='2km', description='20k race'))
        self.assertEqual(running.multi_step.race_generator('20km', 80),
                         running.multi_step.race_steps_generator(z2='8km', z3='10km', z4='2km', description='20k race'))
        self.assertEqual(running.multi_step.race_generator('20km', 90),
                         running.multi_step.race_steps_generator(z2='9km', z3='9km', z4='2km', description='20k race'))
        self.assertEqual(running.multi_step.race_generator('20km', 100),
                         running.multi_step.race_steps_generator(z2='10km', z3='8km', z4='2km', description='20k race'))
        self.assertEqual(running.multi_step.race_generator('20km', 110),
                         running.multi_step.race_steps_generator(z2='11km', z3='7km', z4='2km', description='20k race'))
        self.assertEqual(running.multi_step.race_generator('20km', 120),
                         running.multi_step.race_steps_generator(z2='12km', z3='6km', z4='2km', description='20k race'))
        self.assertEqual(running.multi_step.race_generator('20km', 130),
                         running.multi_step.race_steps_generator(z2='13km', z3='5km', z4='2km', description='20k race'))
        self.assertEqual(running.multi_step.race_generator('21.1km', 80),
                         running.multi_step.race_steps_generator(z2='8km', z3='11km', z4='2.1km',
                                                                 description='Half marathon race'))
        self.assertEqual(running.multi_step.race_generator('21.1km', 90),
                         running.multi_step.race_steps_generator(z2='9km', z3='10km', z4='2.1km',
                                                                 description='Half marathon race'))
        self.assertEqual(running.multi_step.race_generator('21.1km', 100),
                         running.multi_step.race_steps_generator(z2='10km', z3='9km', z4='2.1km',
                                                                 description='Half marathon race'))
        self.assertEqual(running.multi_step.race_generator('21.1km', 110),
                         running.multi_step.race_steps_generator(z2='11km', z3='8km', z4='2.1km',
                                                                 description='Half marathon race'))
        self.assertEqual(running.multi_step.race_generator('21.1km', 120),
                         running.multi_step.race_steps_generator(z2='12km', z3='7km', z4='2.1km',
                                                                 description='Half marathon race'))
        self.assertEqual(running.multi_step.race_generator('21.1km', 130),
                         running.multi_step.race_steps_generator(z2='13km', z3='6km', z4='2.1km',
                                                                 description='Half marathon race'))
        self.assertEqual(running.multi_step.race_generator('21.1km', 140),
                         running.multi_step.race_steps_generator(z2='14km', z3='5km', z4='2.1km',
                                                                 description='Half marathon race'))
        self.assertEqual(running.multi_step.race_generator('marathon', 150),
                         running.multi_step.race_steps_generator(z1='3km', z2='25km', z3='14.2km',
                                                                 description='Marathon race'))
        self.assertEqual(running.multi_step.race_generator('marathon', 195),
                         running.multi_step.race_steps_generator(z1='7km', z2='25km', z3='10.2km',
                                                                 description='Marathon race'))
        self.assertEqual(running.multi_step.race_generator('marathon', 220),
                         running.multi_step.race_steps_generator(z1='10km', z2='25km', z3='7.2km',
                                                                 description='Marathon race'))
        self.assertEqual(running.multi_step.race_generator('marathon', 240),
                         running.multi_step.race_steps_generator(z1='12km', z2='25km', z3='5.2km',
                                                                 description='Marathon race'))
        self.assertEqual(running.multi_step.race_generator('marathon', 250),
                         running.multi_step.race_steps_generator(z1='15km', z2='25km', z3='2.2km',
                                                                 description='Marathon race'))

    def test_extract_duration(self) -> None:
        self.assertEqual(includeloader.extract_duration('1min'), '0:01:00')
        self.assertEqual(includeloader.extract_duration('30s'), '0:00:30')
        self.assertEqual(includeloader.extract_duration('1:00'), '1:00')
        self.assertEqual(includeloader.extract_duration('1km'), '1km')
        self.assertEqual(includeloader.extract_duration('1000m'), '1000m')
        self.assertEqual(includeloader.extract_duration('1k'), '1km')
        self.assertEqual(includeloader.extract_duration('half'), '21.1km')
        self.assertEqual(includeloader.extract_duration('1,5'), '1.5km')

    def test_strength(self) -> None:
        duration = str(4)
        steps: list[dict] = []
        med = str(int(int(duration) / 2))
        steps.append(running.multi_step.step_generator(
            category='PLANK',
            description='Straight Arm Plank With Shoulder Touch',
            duration=duration + 'reps',
            exerciseName='STRAIGHT_ARM_PLANK_WITH_SHOULDER_TOUCH'))
        steps.append(running.multi_step.step_generator(
            category='PUSH_UP',
            duration=med + 'reps',
            description='Push Up',
            exerciseName='PUSH_UP'))
        steps.append(running.multi_step.step_generator(
            category='SHOULDER_STABILITY',
            description='Lying External Rotation',
            duration=duration + 'reps',
            exerciseName='LYING_EXTERNAL_ROTATION'))
        steps.append(running.multi_step.step_generator(
            type='rest',
            duration='2:00'))
        self.assertEqual(strength.multi_step.plank_push_angel_generator(duration), steps)


class TestExerciseGenerator(unittest.TestCase):
    def test_invalid_category(self) -> None:
        with self.assertRaises(KeyError):
            exercise_generator(category='invalid', exercise_name='push_up', duration='10', execution='reps')

    def test_invalid_exercise_name(self) -> None:
        with self.assertRaises(ValueError):
            exercise_generator(category='CARDIO', exercise_name='invalid_exercise', duration='10', execution='reps')
