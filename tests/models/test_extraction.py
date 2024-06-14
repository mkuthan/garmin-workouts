import unittest
from garminworkouts.models.extraction import (end_condition_extraction, target_extraction)


class ExtractionTestCase(unittest.TestCase):
    def test_end_condition_extraction(self) -> None:
        step_json: dict = {
            'endCondition': {
                'conditionTypeKey': 'time'
            },
            'endConditionValue': 60
        }
        step: dict = {}
        expected_result: dict = {
            'duration': '0:01:00'
        }
        self.assertEqual(end_condition_extraction(step_json, step), expected_result)

        step_json = {
            'endCondition': {
                'conditionTypeKey': 'distance'
            },
            'endConditionValue': 5000
        }
        step = {}
        expected_result = {
            'duration': '5.0km'
        }
        self.assertEqual(end_condition_extraction(step_json, step), expected_result)

        step_json = {
            'endCondition': {
                'conditionTypeKey': 'reps'
            },
            'endConditionValue': 10
        }
        step = {}
        expected_result = {
            'duration': '10reps'
        }
        self.assertEqual(end_condition_extraction(step_json, step), expected_result)

        step_json = {
            'endCondition': {
                'conditionTypeKey': 'heart.rate'
            },
            'endConditionValue': 150,
            'endConditionCompare': '>'
        }
        step = {}
        expected_result = {
            'duration': '150ppm>'
        }
        self.assertEqual(end_condition_extraction(step_json, step), expected_result)

        step_json = {
            'endCondition': {
                'conditionTypeKey': 'lap.button',
            },
            'endConditionValue': None,
        }
        step = {}
        expected_result = {
            'duration': 'lap.button',
        }
        self.assertEqual(end_condition_extraction(step_json, step), expected_result)

    def test_target_extraction(self) -> None:
        step_json: dict = {
            'targetType': {
                'workoutTargetTypeKey': 'pace.zone'
            },
            'targetValueOne': 100,
            'targetValueTwo': 200,
            'zoneNumber': None
        }
        step: dict = {}
        expected_result: dict = {
            'target': {
                'type': 'pace.zone',
                'min': '0:00:10',
                'max': '0:00:05'
            }
        }
        self.assertEqual(target_extraction(step_json, step), expected_result)

        step_json = {
            'targetType': {
                'workoutTargetTypeKey': 'cadence'
            },
            'targetValueOne': 80,
            'targetValueTwo': 100
        }
        step = {}
        expected_result = {
            'target': {
                'type': 'cadence',
                'min': '80',
                'max': '100'
            }
        }
        self.assertEqual(target_extraction(step_json, step), expected_result)

        step_json = {
            'targetType': {
                'workoutTargetTypeKey': 'heart.rate.zone'
            },
            'zoneNumber': 2,
            'targetValueOne': 120,
            'targetValueTwo': 150
        }
        step = {}
        expected_result = {
            'target': {
                'type': 'heart.rate.zone',
                'zone': '2',
            }
        }
        self.assertEqual(target_extraction(step_json, step), expected_result)

        step_json = {
            'targetType': {
                'workoutTargetTypeKey': 'power.zone'
            },
            'zoneNumber': 3,
            'targetValueOne': 200,
            'targetValueTwo': 250
        }
        step = {}
        expected_result = {
            'target': {
                'type': 'power.zone',
                'zone': '3'
            }
        }
        self.assertEqual(target_extraction(step_json, step), expected_result)
