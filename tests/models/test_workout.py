import unittest

from garminworkouts.models.workout import Workout


class WorkoutTestCase(unittest.TestCase):
    def test_create_workout(self):
        config = {
            "name": "Any workout name",
            "steps": [{"power": 50, "duration": "1:00"}, {"power": 60, "duration": "2:00"}],
        }

        ftp = 200
        power_target_diff = 0.05

        workout = Workout(config, ftp, power_target_diff)

        workout_id = "any workout id"
        workout_owner_id = "any workout owner id"
        payload = workout.create_workout(workout_id, workout_owner_id)

        expected_workout_payload = {
            "workoutId": workout_id,
            "ownerId": workout_owner_id,
            "workoutName": "Any workout name",
            "description": "FTP 200, TSS 1, NP 114, IF 0.57",
            "sportType": {"sportTypeId": 2, "sportTypeKey": "cycling"},
            "workoutSegments": [
                {
                    "segmentOrder": 1,
                    "sportType": {"sportTypeId": 2, "sportTypeKey": "cycling"},
                    "workoutSteps": [
                        {
                            "type": "ExecutableStepDTO",
                            "stepOrder": 1,
                            "stepType": {"stepTypeId": 3, "stepTypeKey": "interval"},
                            "childStepId": None,
                            "endCondition": {"conditionTypeId": 2, "conditionTypeKey": "time"},
                            "endConditionValue": 60,
                            "targetType": {"workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone"},
                            "targetValueOne": 95,
                            "targetValueTwo": 105,
                        },
                        {
                            "type": "ExecutableStepDTO",
                            "stepOrder": 2,
                            "stepType": {"stepTypeId": 3, "stepTypeKey": "interval"},
                            "childStepId": None,
                            "endCondition": {"conditionTypeId": 2, "conditionTypeKey": "time"},
                            "endConditionValue": 120,
                            "targetType": {"workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone"},
                            "targetValueOne": 114,
                            "targetValueTwo": 126,
                        },
                    ],
                }
            ],
        }

        self.assertDictEqual(payload, expected_workout_payload)

    def test_create_workout_preserves_adjacent_equal_steps(self):
        interval = {"power": 50, "duration": "1:00"}
        config = {
            "name": "Repeated intervals",
            "steps": [interval, interval.copy(), {"power": 60, "duration": "2:00"}, interval, interval],
        }

        payload = Workout(config, 200, 0.05).create_workout()
        steps = payload["workoutSegments"][0]["workoutSteps"]

        self.assertEqual([step["endConditionValue"] for step in steps], [60, 60, 120, 60, 60])
        self.assertEqual([step["stepOrder"] for step in steps], [1, 2, 3, 4, 5])
        self.assertTrue(all(step["type"] == "ExecutableStepDTO" for step in steps))
        self.assertTrue(all(step["childStepId"] is None for step in steps))

    def test_create_workout_preserves_equal_steps_in_repeated_groups(self):
        interval = {"power": 70, "duration": "1:00"}
        group = [interval, interval.copy(), {"power": 80, "duration": "2:00"}]
        config = {
            "name": "Repeated groups",
            "steps": [{"power": 50, "duration": "1:00"}, group, group, {"power": 50, "duration": "1:00"}],
        }

        payload = Workout(config, 200, 0.05).create_workout()
        steps = payload["workoutSegments"][0]["workoutSteps"]

        self.assertEqual(len(steps), 3)
        repeated_group = steps[1]
        self.assertEqual(repeated_group["type"], "RepeatGroupDTO")
        self.assertEqual(repeated_group["numberOfIterations"], 2)
        nested_steps = repeated_group["workoutSteps"]
        self.assertEqual([step["endConditionValue"] for step in nested_steps], [60, 60, 120])
        self.assertEqual([step["stepOrder"] for step in steps], [1, 2, 6])
        self.assertEqual([step["stepOrder"] for step in nested_steps], [3, 4, 5])
        self.assertTrue(all(step["childStepId"] == repeated_group["childStepId"] for step in nested_steps))

    def test_create_workout_preserves_adjacent_lap_button_steps(self):
        config = {
            "name": "Lap button intervals",
            "steps": [{"power": 50, "duration": "1:00"}, {"power": 70}, {"power": 70}],
        }

        payload = Workout(config, 200, 0.05).create_workout()
        steps = payload["workoutSegments"][0]["workoutSteps"]

        self.assertEqual(
            [step["endCondition"]["conditionTypeKey"] for step in steps], ["time", "lap.button", "lap.button"]
        )
        self.assertEqual([step["endConditionValue"] for step in steps], [60, None, None])


if __name__ == "__main__":
    unittest.main()
