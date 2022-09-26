import unittest

from garminworkouts.models.workout import Workout


class WorkoutTestCase(unittest.TestCase):
    def test_create_workout(self):
        config = {
            'name': 'Any workout name',
            'steps': [
                {'power': 50, 'duration': '1:00'},
                {'power': 60, 'duration': '2:00'}
            ]
        }

        ftp = 200
        power_target_diff = 0.05

        workout = Workout(config, ftp, power_target_diff)

        workout_id = "any workout id"
        workout_owner_id = "any workout owner id"
        payload = workout.create_workout(workout_id, workout_owner_id)

        expected_workout_payload = {
            'workoutId': workout_id,
            'ownerId': workout_owner_id,
            'workoutName': 'Any workout name',
            'description': 'FTP 200, TSS 1, NP 114, IF 0.57',
            'sportType': {'sportTypeId': 2, 'sportTypeKey': 'cycling'},
            'workoutSegments': [
                {
                    'segmentOrder': 1,
                    'sportType': {'sportTypeId': 2, 'sportTypeKey': 'cycling'},
                    'workoutSteps': [
                        {'type': 'ExecutableStepDTO', 'stepOrder': 1,
                         'stepType': {'stepTypeId': 3, 'stepTypeKey': 'interval'}, 'childStepId': None,
                         'endCondition': {'conditionTypeId': 2, 'conditionTypeKey': 'time'}, 'endConditionValue': 60,
                         'targetType': {'workoutTargetTypeId': 2, 'workoutTargetTypeKey': 'power.zone'},
                         'targetValueOne': 95, 'targetValueTwo': 105},
                        {'type': 'ExecutableStepDTO', 'stepOrder': 2,
                         'stepType': {'stepTypeId': 3, 'stepTypeKey': 'interval'}, 'childStepId': None,
                         'endCondition': {'conditionTypeId': 2, 'conditionTypeKey': 'time'}, 'endConditionValue': 120,
                         'targetType': {'workoutTargetTypeId': 2, 'workoutTargetTypeKey': 'power.zone'},
                         'targetValueOne': 114, 'targetValueTwo': 126}
                    ]
                }
            ]
        }

        self.assertDictEqual(payload, expected_workout_payload)


if __name__ == '__main__':
    unittest.main()
