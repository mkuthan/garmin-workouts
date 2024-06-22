import unittest
import os
from garminworkouts.models.extraction import Extraction
from garminworkouts.config import configreader


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
        self.assertEqual(Extraction.end_condition_extraction(step_json, step), expected_result)

        step_json: dict = {
            'endCondition': {
                'conditionTypeKey': 'fixed.rest'
            },
            'endConditionValue': 60
        }
        step: dict = {}
        expected_result: dict = {
            'duration': '0:01:00'
        }
        self.assertEqual(Extraction.end_condition_extraction(step_json, step), expected_result)

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
        self.assertEqual(Extraction.end_condition_extraction(step_json, step), expected_result)

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
        self.assertEqual(Extraction.end_condition_extraction(step_json, step), expected_result)

        step_json = {
            'endCondition': {
                'conditionTypeKey': 'calories'
            },
            'endConditionValue': 10
        }
        step = {}
        expected_result = {
            'duration': '10cal'
        }
        self.assertEqual(Extraction.end_condition_extraction(step_json, step), expected_result)

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
        self.assertEqual(Extraction.end_condition_extraction(step_json, step), expected_result)

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
        self.assertEqual(Extraction.end_condition_extraction(step_json, step), expected_result)

        for condition in ('power', 'iterations', 'fixed.repetition', 'power', 'iterations',
                          'training.peaks.tss', 'repetition.time', 'time.at.valid.cda', 'power.last.lap',
                          'max.power.last.lap', 'repetition.swim.css.offset'):
            step_json = {
                'endCondition': {
                    'conditionTypeKey': condition
                },
                'endConditionValue': 10
            }
            step = {}
            with self.assertRaises(ValueError):
                Extraction.end_condition_extraction(step_json, step)

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
        self.assertEqual(Extraction.target_extraction(step_json, step), expected_result)

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
        self.assertEqual(Extraction.target_extraction(step_json, step), expected_result)

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
        self.assertEqual(Extraction.target_extraction(step_json, step), expected_result)

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
        self.assertEqual(Extraction.target_extraction(step_json, step), expected_result)

        step_json: dict = {
            'targetType': {
                'workoutTargetTypeKey': 'no.target'
            }
        }
        step: dict = {}
        expected_result: dict = {
            'target': {
                'type': 'no.target'
            }
        }
        self.assertEqual(Extraction.target_extraction(step_json, step), expected_result)

        for target in ('speed.zone', 'grade', 'heart.rate.lap', 'power.lap', 'power.3s', 'power.10s', 'power.30s',
                       'speed.lap', 'swim.stroke', 'resistance', 'power.curve', 'swim.css.offset', 'swim.instruction'):
            step_json = {
                'targetType': {
                    'workoutTargetTypeKey': target
                }
            }
            step = {}

            with self.assertRaises(ValueError):
                Extraction.target_extraction(step_json, step)

    def test_secondary_target_extraction(self) -> None:
        step_json: dict = {
            'secondaryTargetType': {
                'workoutTargetTypeKey': 'no.target'
            },
        }
        step: dict = {}
        expected_result: dict = {
            'secondaryTarget': {
                'type': 'no.target',
            }
        }
        self.assertEqual(Extraction.secondary_target_extraction(step_json, step), expected_result)

        step_json: dict = {
            'secondaryTargetType': {
                'workoutTargetTypeKey': 'pace.zone'
            },
            'secondaryTargetValueOne': 100,
            'secondaryTargetValueTwo': 200,
            'secondaryZoneNumber': None
        }
        step: dict = {}
        expected_result: dict = {
            'secondaryTarget': {
                'type': 'pace.zone',
                'min': '0:00:10',
                'max': '0:00:05'
            }
        }
        self.assertEqual(Extraction.secondary_target_extraction(step_json, step), expected_result)

        step_json = {
            'secondaryTargetType': {
                'workoutTargetTypeKey': 'cadence'
            },
            'secondaryTargetValueOne': 80,
            'secondaryTargetValueTwo': 100
        }
        step = {}
        expected_result = {
            'secondaryTarget': {
                'type': 'cadence',
                'min': '80',
                'max': '100'
            }
        }
        self.assertEqual(Extraction.secondary_target_extraction(step_json, step), expected_result)

        step_json = {
            'secondaryTargetType': {
                'workoutTargetTypeKey': 'heart.rate.zone'
            },
            'secondaryZoneNumber': 2,
            'secondaryTargetValueOne': 120,
            'secondaryTargetValueTwo': 150
        }
        step = {}
        expected_result = {
            'secondaryTarget': {
                'type': 'heart.rate.zone',
                'zone': '2',
            }
        }
        self.assertEqual(Extraction.secondary_target_extraction(step_json, step), expected_result)

        step_json = {
            'secondaryTargetType': {
                'workoutTargetTypeKey': 'power.zone'
            },
            'secondaryZoneNumber': 3,
            'secondaryTargetValueOne': 200,
            'secondaryTargetValueTwo': 250
        }
        step = {}
        expected_result = {
            'secondaryTarget': {
                'type': 'power.zone',
                'zone': '3'
            }
        }
        self.assertEqual(Extraction.secondary_target_extraction(step_json, step), expected_result)

        for target in ('speed.zone', 'grade', 'heart.rate.lap', 'power.lap', 'power.3s', 'power.10s', 'power.30s',
                       'speed.lap', 'swim.stroke', 'resistance', 'power.curve', 'swim.css.offset', 'swim.instruction'):
            step_json = {
                'secondaryTargetType': {
                    'workoutTargetTypeKey': target
                }
            }
            step = {}
            with self.assertRaises(ValueError):
                Extraction.secondary_target_extraction(step_json, step)

    def test_weight_extraction(self) -> None:
        step_json: dict = {
            'weightValue': '75',
            'weightUnit': {
                'unitKey': 'kilogram'
            }
        }
        step: dict = {}
        expected_result: dict = {
            'weight': '75kg'
        }
        self.assertEqual(Extraction.weight_extraction(step_json, step), expected_result)

        step_json = {
            'weightValue': '150',
            'weightUnit': {
                'unitKey': 'pound'
            }
        }
        step = {}
        expected_result = {
            'weight': '150pound'
        }
        self.assertEqual(Extraction.weight_extraction(step_json, step), expected_result)

        step_json = {
            'weightValue': '100',
            'weightUnit': {
                'unitKey': 'invalid'
            }
        }
        step = {}
        with self.assertRaises(ValueError):
            Extraction.weight_extraction(step_json, step)

    def test_workout_export_yaml(self) -> None:
        # Test case 1
        workout: dict = {
            'workoutName': 'Test Workout',
            'sportType': {'sportTypeKey': 'running'},
            'description': 'This is a test workout',
            'workoutSegments': [
                {
                    'workoutSteps': [
                        {
                            'stepType': {'stepTypeKey': 'step'},
                            'endCondition': {'conditionTypeKey': 'time'},
                            'endConditionValue': 60,
                            'targetType': {'workoutTargetTypeKey': 'pace.zone'},
                            'targetValueOne': 100,
                            'targetValueTwo': 200,
                            'zoneNumber': None
                        },
                        {
                            'stepType': {'stepTypeKey': 'step'},
                            'endCondition': {'conditionTypeKey': 'distance'},
                            'endConditionValue': 5000,
                            'targetType': {'workoutTargetTypeKey': 'cadence'},
                            'targetValueOne': 80,
                            'targetValueTwo': 100
                        },
                        {
                            'stepType': {'stepTypeKey': 'repeat'},
                            'workoutSteps': [
                                {
                                    'stepType': {'stepTypeKey': 'step'},
                                    'endCondition': {'conditionTypeKey': 'time'},
                                    'endConditionValue': 60,
                                    'targetType': {'workoutTargetTypeKey': 'pace.zone'},
                                    'targetValueOne': 100,
                                    'targetValueTwo': 200,
                                    'zoneNumber': None
                                }
                            ],
                        },
                        {
                            'stepType': {'stepTypeKey': 'repeat'},
                            'numberOfIterations': 1,
                            'workoutSteps': [
                                {
                                    'stepType': {'stepTypeKey': 'step'},
                                    'endCondition': {'conditionTypeKey': 'time'},
                                    'endConditionValue': 60,
                                    'targetType': {'workoutTargetTypeKey': 'pace.zone'},
                                    'targetValueOne': 100,
                                    'targetValueTwo': 200,
                                    'zoneNumber': None
                                }
                            ],
                        }
                    ]
                }
            ]
        }
        filename = 'test_workout.yaml'
        expected_output: dict = {
            'description': 'This is a test workout',
            'name': 'Test Workout',
            'sport': 'running',
            'steps': [
                {
                    'duration': '0:01:00',
                    'target': {
                        'max': '0:00:05',
                        'min': '0:00:10',
                        'type': 'pace.zone'
                        },
                    'type': 'step'},
                {
                    'duration': '5.0km',
                    'target': {'max': '100', 'min': '80', 'type': 'cadence'},
                    'type': 'step'
                },
                {
                    'duration': '0:01:00',
                    'repeatDuration': '0:00:00',
                    'target': {'max': '0:00:05', 'min': '0:00:10', 'type': 'pace.zone'},
                    'type': 'step'
                },
                [{
                    'duration': '0:01:00',
                    'target': {'max': '0:00:05', 'min': '0:00:10', 'type': 'pace.zone'}, 'type': 'step'}]
                ]
        }

        # Call the function
        Extraction.workout_export_yaml(workout, filename)

        # Read the generated YAML file
        generated_yaml: dict = configreader.read_config(filename)

        # Assert the generated YAML matches the expected output
        self.assertEqual(generated_yaml, expected_output)

        os.remove(filename)

    def test_event_export_yaml(self):
        event: dict = {
            'name': 'Test Event',
            'date': '2022-01-01',
            'location': 'Test Location'
        }
        filename = 'test_event.yaml'

        expected_output: dict = {
            'name': 'Test Event',
            'date': '2022-01-01',
            'location': 'Test Location'
        }

        # Call the function here
        Extraction.event_export_yaml(event, filename)

        # Read the generated YAML file
        generated_yaml: dict = configreader.read_config(filename)

        # Assert the generated YAML matches the expected output
        self.assertEqual(generated_yaml, expected_output)

        os.remove(filename)

    def test_note_export_yaml(self) -> None:
        note: dict = {
            'note_name': 'Test Note',
            'note_content': 'Test Content'
        }
        filename = 'test_note.yaml'

        expected_output: dict = {
            'note_name': 'Test Note',
            'note_content': 'Test Content'
        }
        # Call the function here
        Extraction.note_export_yaml(note, filename)

        # Read the generated YAML file
        generated_yaml: dict = configreader.read_config(filename)

        # Assert the generated YAML matches the expected output
        self.assertEqual(generated_yaml, expected_output)

        os.remove(filename)


'''    def test_workout_export_yaml(self) -> None:
        workout = {
            'workoutName': 'My Workout',
            'sportType': {'sportTypeKey': 'running'},
            'description': 'This is a test workout',
            'workoutSegments': [
                {
                    'workoutSteps': [
                        {
                            'stepType': {'stepTypeKey': 'step'},
                            'endCondition': {'conditionTypeKey': 'time'},
                            'endConditionValue': 60
                        },
                        {
                            'stepType': {'stepTypeKey': 'step'},
                            'endCondition': {'conditionTypeKey': 'distance'},
                            'endConditionValue': 5000
                        }
                    ]
                }
            ]
        }
        filename = 'test_workout.yaml'
        Extraction.workout_export_yaml(workout, filename)

        with open(filename, 'r') as file:
            exported_workout = yaml.safe_load(file)

        expected_workout = {
            'name': 'My Workout',
            'sport': 'running',
            'description': 'This is a test workout',
            'steps': [
                {
                    'type': 'step',
                    'duration': '0:01:00'
                },
                {
                    'type': 'step',
                    'duration': '5.0km'
                }
            ]
        }

        self.assertEqual(exported_workout, expected_workout)
'''
