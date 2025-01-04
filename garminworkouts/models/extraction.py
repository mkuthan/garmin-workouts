from datetime import timedelta
import yaml
from typing import Any


class Extraction(object):
    @staticmethod
    def description_formatting(description: str | None) -> str:
        if description is None:
            return ''

        if 'rest20s' in description:
            description = description.replace('rest20s', 'rest\n 20s')
        if not any(substring in description for substring in ['Dr.', '. Complete', '\u2022']):
            description = description.replace('. ', '.\n').replace('.\n', '.\n ')
        if '.Try' in description:
            description = description.replace('.Try', '.\nTry')
        if ':20s' in description:
            description = description.replace(':20s', ':\n-20s')
        if '.8 sets' in description:
            description = description.replace('.8 sets', '.\n-8 sets')
        if ')8 sets' in description:
            description = description.replace(')8 sets', ')\n-8 sets')
        if '.Workout' in description:
            description = description.replace('.Workout', '.\nWorkout')
        if 'push-ups.Benchmark' in description:
            description = description.replace('push-ups.Benchmark', 'push-ups.\nBenchmark')
        return description

    @staticmethod
    def end_condition_extraction(step_json, step) -> dict:
        end_condition: str = step_json['endCondition']['conditionTypeKey']
        end_condition_value: Any = step_json['endConditionValue']

        if end_condition == 'time' or end_condition == 'fixed.rest':
            step['duration'] = str(timedelta(seconds=int(end_condition_value)))
        elif end_condition == 'distance':
            step['duration'] = f"{round(float(end_condition_value) / 1000, 3)}km"
        elif end_condition == 'reps':
            step['duration'] = f"{int(end_condition_value)}reps"
        elif end_condition == 'heart.rate':
            step['duration'] = f"{int(end_condition_value)}ppm{step_json['endConditionCompare']}"
        elif end_condition == 'calories':
            step['duration'] = f"{int(end_condition_value)}cal"
        elif end_condition == 'lap.button':
            step['duration'] = 'lap.button'
        else:
            raise ValueError(f"Unsupported end condition: {end_condition}")

        return step

    @staticmethod
    def target_extraction(step_json, step) -> dict:
        step['target'] = {}
        step['target']['type'] = 'no.target'
        if 'targetType' in step_json and step_json['targetType']:
            target_type_key: Any = step_json['targetType']['workoutTargetTypeKey']

            if target_type_key == 'pace.zone':
                step['target'] = {
                    'type': target_type_key,
                    **({'min': str(timedelta(seconds=1000 / float(step_json.get('targetValueOne'))))}
                        if step_json.get(step_json['zoneNumber'], None) is None else {}),
                    **({'max': str(timedelta(seconds=1000 / float(step_json.get('targetValueTwo'))))}
                       if step_json.get(step_json['zoneNumber'], None) is None else {}),
                }

            elif target_type_key == 'cadence':
                step['target'] = {
                    'type': target_type_key,
                    'min': str(int(step_json.get('targetValueOne', None))),
                    'max': str(int(step_json.get('targetValueTwo', None)))
                }

            elif target_type_key in ['heart.rate.zone', 'power.zone']:
                step['target'] = {
                    'type': target_type_key,
                    **({'min': str(int(step_json.get('targetValueOne', None)))}
                        if step_json.get('zoneNumber', None) is None else {}),
                    **({'max': str(int(step_json.get('targetValueTwo', None)))}
                        if step_json.get('zoneNumber', None) is None else {}),
                    ** ({'zone': str(step_json.get('zoneNumber', None))}
                        if step_json.get('zoneNumber', None) is not None else {})
                }

            elif target_type_key == 'no.target':
                step['target']['type'] = 'no.target'

            else:
                raise ValueError(f"Unsupported target: {target_type_key}")

        return step

    @staticmethod
    def secondary_target_extraction(step_json, step) -> dict:
        if 'secondaryTargetType' in step_json and step_json['secondaryTargetType']:
            secondary_target_key: Any = step_json['secondaryTargetType']['workoutTargetTypeKey']
            if secondary_target_key == 'pace.zone':
                step['secondaryTarget'] = {
                    'type': secondary_target_key,
                    **({'min': str(timedelta(seconds=1000 / float(step_json.get('secondaryTargetValueOne'))))}
                        if step_json.get('secondaryZoneNumber', None) is None else {}),
                    **({'max': str(timedelta(seconds=1000 / float(step_json.get('secondaryTargetValueTwo'))))}
                       if step_json.get('secondaryZoneNumber', None) is None else {}),
                }

            elif secondary_target_key == 'cadence':
                step['secondaryTarget'] = {
                    'type': secondary_target_key,
                    'min': str(int(step_json.get('secondaryTargetValueOne', None))),
                    'max': str(int(step_json.get('secondaryTargetValueTwo', None)))
                }

            elif secondary_target_key in ['heart.rate.zone', 'power.zone']:
                step['secondaryTarget'] = {
                    'type': secondary_target_key,
                    ** ({'min': str(int(step_json.get('secondaryTargetValueOne', None)))}
                        if step_json.get('secondaryZoneNumber', None) is None else {}),
                    **({'max': str(int(step_json.get('secondaryTargetValueTwo', None)))}
                        if step_json.get('secondaryZoneNumber', None) is None else {}),
                    ** ({'zone': str(step_json.get('secondaryZoneNumber', None))}
                        if step_json.get('secondaryZoneNumber', None) is not None else {})
                }

            elif secondary_target_key == 'no.target':
                step.pop('secondaryTarget', None)

            else:
                raise ValueError(f"Unsupported secondary target: {secondary_target_key}")
        return step

    @staticmethod
    def weight_extraction(step_json, step) -> dict:
        weight_value: str | None = step_json.get('weightValue')
        weight_unit: str | None = step_json.get('weightUnit', {}
                                                ).get('unitKey') if step_json.get('weightUnit') else None
        if weight_value is not None:
            if weight_unit == 'kilogram':
                step['weight'] = f"{weight_value}kg"
            elif weight_unit == 'pound':
                step['weight'] = f"{weight_value}pound"
            else:
                raise ValueError(f"Unsupported weight unit: {weight_unit}")
        return step

    @staticmethod
    def step_extraction(step_json) -> dict | None:
        if step_json['stepType']['stepTypeKey'] != 'repeat':
            step: dict = {
                'type': step_json['stepType']['stepTypeKey'],
                **({'description': step_json.get('description', '')}
                   if step_json.get('description') else {}),
                **({'equipment': step_json.get('equipmentType', {}).get('equipmentTypeKey')}
                   if step_json.get('equipmentType', {}).get('equipmentTypeKey') else {}),
                **({'category': step_json.get('category')}
                   if step_json.get('category') else {}),
                **({'exerciseName': step_json.get('exerciseName')}
                    if step_json.get('exerciseName') else {}),
                # **({'workoutProvider': step_json.get('workoutProvider')}
                #   if step_json.get('workoutProvider') else {}),
                # **({'providerExerciseSourceId': step_json.get('providerExerciseSourceId')}
                #   if step_json.get('providerExerciseSourceId') else {}),
                **({'repeatDuration': step_json.get('repeatDuration')}
                   if step_json.get('repeatDuration') else {}),
            }
            step = Extraction.end_condition_extraction(step_json, step)
            step = Extraction.target_extraction(step_json, step)
            step = Extraction.secondary_target_extraction(step_json, step)
            step = Extraction.weight_extraction(step_json, step)
            return step

    @staticmethod
    def workout_export_yaml(workout, filename) -> None:
        workout_dict: dict = {
            'name': workout.get('workoutName', ''),
            'sport': workout['sportType'].get('sportTypeKey', ''),
            **({'subsport': workout.get('subSportType', '') if 'subSportType' in workout else ''}
               if workout.get('subSportType', '') else {}),
            'description': Extraction.description_formatting(workout.get('description', '')),
            'steps': [],
        }

        if 'workoutSegments' in workout and workout['workoutSegments']:
            workout_segment: Any = workout['workoutSegments'][0]
            workout_steps: Any = workout_segment.get('workoutSteps', [])

            for step_json in workout_steps:
                step_type: Any = step_json['stepType'].get('stepTypeKey', '')

                if step_type != 'repeat':
                    workout_dict['steps'].append(Extraction.step_extraction(step_json))
                else:
                    if 'numberOfIterations' in step_json and step_json['numberOfIterations'] is not None:
                        rep_step = [Extraction.step_extraction(rep_step_json)
                                    for rep_step_json in step_json.get('workoutSteps', [])]
                        for _ in range(step_json['numberOfIterations']):
                            workout_dict['steps'].append(rep_step)
                    else:
                        for rep_step_json in step_json.get('workoutSteps', []):
                            rep_step_json['repeatDuration'] = str(timedelta(seconds=int(
                                step_json.get('endConditionValue', 0))))
                            workout_dict['steps'].append(Extraction.step_extraction(rep_step_json))
        with open(filename, 'w') as file:
            yaml.dump(workout_dict, file, default_flow_style=None)

    @staticmethod
    def event_export_yaml(event, filename) -> None:
        with open(filename, 'w') as file:
            yaml.dump(event, file, default_flow_style=None)

    @staticmethod
    def note_export_yaml(note, filename) -> None:
        with open(filename, 'w') as file:
            yaml.dump(note, file, default_flow_style=False)
