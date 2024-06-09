import unittest

from garminworkouts.models.fields import TARGET_TYPES, get_target_type, _WORKOUT_TARGET
from garminworkouts.models.target import Target


class TestTarget(unittest.TestCase):
    def test_get_target_type(self) -> None:
        for target_type in TARGET_TYPES.keys():
            with self.subTest('Test types'):
                TT: dict = {
                    f"{_WORKOUT_TARGET}Id": TARGET_TYPES[target_type],
                    f"{_WORKOUT_TARGET}Key": target_type,
                }
                self.assertDictEqual(TT, get_target_type(target_type))

    def test_create_target_assertions(self) -> None:
        targets: list[dict] = [
            {'target': 'no.targe', 'value_one': None, 'value_two': None, 'zone': None, 'secondary': False},
            {'target': 'heart.rate', 'value_one': 120, 'value_two': None, 'zone': None, 'secondary': False},
            {'target': 'heart.rate', 'value_one': None, 'value_two': 120, 'zone': None, 'secondary': False},
            {'target': 'heart.rate', 'value_one': '120', 'value_two': None, 'zone': None, 'secondary': False},
            {'target': 'heart.rate', 'value_one': '120', 'value_two': '125', 'zone': None, 'secondary': False},
            {'target': 'heart.rate', 'value_one': 125, 'value_two': 121, 'zone': 1, 'secondary': False},
            {'target': 'heart.rate.zone', 'value_one': 125, 'value_two': 121, 'zone': 6, 'secondary': False},
            {'target': 'heart.rate.zone', 'value_one': 125, 'value_two': 121, 'zone': None, 'secondary': False},
            {'target': 'pace.zone', 'value_one': 3, 'value_two': 3.1, 'zone': 6, 'secondary': False},
        ]

        for target_def in targets:
            with self.subTest(msg="Expected ValueError for '%s" % target_def):
                with self.assertRaises(TypeError):
                    Target(target=target_def['target'],
                           value_one=target_def['value_one'],
                           value_two=target_def['value_two'],
                           zone=target_def['zone'],
                           secondary=target_def['secondary'])

    def test_init_positive(self) -> None:
        target = Target(target='power.zone', value_one=100, value_two=200, zone=None, secondary=False)
        self.assertEqual(target.target, 'power.zone')
        self.assertEqual(target.value_one, 100)
        self.assertEqual(target.value_two, 200)
        self.assertIsNone(target.zone)
        self.assertFalse(target.secondary)

    def test_init_negative(self) -> None:
        with self.assertRaises(TypeError):
            Target(target='invalid_target_type', value_one=100, value_two=200, zone=None, secondary=False)

    def test_create_target_no_target(self) -> None:
        target = Target(target='no.target')
        self.assertEqual(target.create_target(), {})

    def test_create_target_with_target(self) -> None:
        target = Target(target='power.zone', value_one=100, value_two=200, zone=None, secondary=False)
        expected_output: dict = {
            'targetType': {
                'workoutTargetTypeId': 2,
                'workoutTargetTypeKey': 'power.zone'
                },
            'targetValueOne': 100,
            'targetValueTwo': 200,
            'zoneNumber': None}
        self.assertEqual(target.create_target(), expected_output)

    def test_invalid_zone_value(self) -> None:
        with self.assertRaises(TypeError):
            Target(target='heart.rate.zone', value_one=100, value_two=200, zone=6, secondary=False)

    def test_invalid_value_order(self) -> None:
        with self.assertRaises(TypeError):
            Target(target='heart.rate.zone', value_one=200, value_two=100, zone=None, secondary=False)
            Target(target='pace.zone', value_one=100, value_two=200, zone=6, secondary=False)

    def test_invalid_numeric_type(self) -> None:
        with self.assertRaises(TypeError):
            Target(target='power.zone', value_one='100', value_two=200, zone=None, secondary=True)
            Target(target='power.zone', value_one='100', value_two='200', zone=None, secondary=True)
            Target(target='power.zone', value_one=100, value_two='200', zone=None, secondary=True)


if __name__ == '__main__':
    unittest.main()
