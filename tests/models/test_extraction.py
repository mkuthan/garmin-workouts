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

        expected_result = {
            'secondaryTarget': {
                'type': 'power.zone',
                'zone': '3'
            }
        }
        self.assertEqual(Extraction.secondary_target_extraction(step_json, step), expected_result)

        step_json = {
            'secondaryTargetType': {
                'workoutTargetTypeKey': 'no.target'
            },
        }

        expected_result = {}
        self.assertEqual(Extraction.secondary_target_extraction(step_json, step), expected_result)

        for target in ('speed.zone', 'grade', 'heart.rate.lap', 'power.lap', 'power.3s', 'power.10s', 'power.30s',
                       'speed.lap', 'swim.stroke', 'resistance', 'power.curve', 'swim.css.offset', 'swim.instruction'):
            step_json = {
                'secondaryTargetType': {
                    'workoutTargetTypeKey': target
                }
            }

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

    def test_description_formatting(self) -> None:
        # Test case 1: description is None
        description = None
        expected_result = ''
        self.assertEqual(Extraction.description_formatting(description), expected_result)

        # Test case 2: description contains 'rest20s'
        description = 'This is a rest20s test.'
        expected_result = 'This is a rest\n 20s test.'
        self.assertEqual(Extraction.description_formatting(description), expected_result)

        # Test case 3: description does not contain 'Dr.', '. Complete', or '\u2022'
        description = 'This is a test. Complete the task.'
        expected_result = 'This is a test. Complete the task.'
        self.assertEqual(Extraction.description_formatting(description), expected_result)

        # Test case 4: description contains '.Try'
        description = 'This is a test.Try to complete it.'
        expected_result = 'This is a test.\nTry to complete it.'
        self.assertEqual(Extraction.description_formatting(description), expected_result)

        # Test case 5: description contains ':20s'
        description = 'Run for 5:20s.'
        expected_result = 'Run for 5:\n-20s.'
        self.assertEqual(Extraction.description_formatting(description), expected_result)

        # Test case 6: description contains '.8 sets'
        description = 'Do this exercise.8 sets of it.'
        expected_result = 'Do this exercise.\n-8 sets of it.'
        self.assertEqual(Extraction.description_formatting(description), expected_result)

        # Test case 7: description contains ')8 sets'
        description = 'Complete the cycle)8 sets.'
        expected_result = 'Complete the cycle)\n-8 sets.'
        self.assertEqual(Extraction.description_formatting(description), expected_result)

        # Test case 8: description contains '.Workout'
        description = 'This is a test.Workout session.'
        expected_result = 'This is a test.\nWorkout session.'
        self.assertEqual(Extraction.description_formatting(description), expected_result)

        # Test case 9: description contains 'push-ups.Benchmark'
        description = 'Do push-ups.Benchmark your progress.'
        expected_result = 'Do push-ups.\nBenchmark your progress.'
        self.assertEqual(Extraction.description_formatting(description), expected_result)

        # Test case 10: description contains multiple patterns
        description = 'This is a rest20s test. Complete the task.Try to finish it:20s.8 sets)8 sets.Workout session.\
            push-ups.Benchmark'
        expected_result = (
            'This is a rest\n 20s test. Complete the task.\nTry to finish it:\n-20s.\n-8 sets)\n-8 sets.\n'
            'Workout session.            push-ups.\nBenchmark'
        )
        self.assertEqual(Extraction.description_formatting(description), expected_result)
