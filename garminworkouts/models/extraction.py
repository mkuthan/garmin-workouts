from datetime import timedelta
import yaml


@staticmethod
def end_condition_extraction(step_json, step) -> dict:
    end_condition: str = step_json['endCondition']['conditionTypeKey']
    end_condition_value = step_json['endConditionValue']

    if end_condition == 'time' or end_condition == 'fixed.rest':
        step['duration'] = str(timedelta(seconds=int(end_condition_value)))
    elif end_condition == 'distance':
        step['duration'] = f"{round(float(end_condition_value) / 1000, 3)}km"
    elif end_condition == 'reps':
        step['duration'] = f"{int(end_condition_value)}reps"
    elif end_condition == 'heart.rate':
        step['duration'] = f"{int(end_condition_value)}ppm{step_json['endConditionCompare']}"
    elif end_condition != 'lap.button':
        step['duration'] = 'lap.button'

    return step


@staticmethod
def target_extraction(step_json, step) -> dict:
    step['target'] = {}
    step['target']['type'] = 'no.target'

    if 'targetType' in step_json and step_json['targetType']:
        target_type_key = step_json['targetType']['workoutTargetTypeKey']
        step['target']['type'] = target_type_key

        if target_type_key == 'pace.zone':
            step['target']['min'] = str(timedelta(seconds=1000 / float(step_json['targetValueOne'])))[2:]
            step['target']['max'] = str(timedelta(seconds=1000 / float(step_json['targetValueTwo'])))[2:]

        elif target_type_key == 'cadence':
            step['target']['min'] = str(int(step_json.get('targetValueOne', None)))
            step['target']['max'] = str(int(step_json.get('targetValueTwo', None)))

        elif target_type_key in ['heart.rate.zone', 'power.zone']:
            step['target']['zone'] = str(step_json.get('zoneNumber', None))
            step['target']['min'] = str(int(step_json.get('targetValueOne', None)))
            step['target']['max'] = str(int(step_json.get('targetValueTwo', None)))

        elif target_type_key not in ['lap.button', 'no.target']:
            print(target_type_key)
            print(step)

    return step


def secondary_target_extraction(step_json, step) -> dict:
    if 'secondaryTargetType' in step_json and step_json['secondaryTargetType'] is not None:
        secondary_target = step['secondaryTarget'] = {}
        secondary_target_type = step_json['secondaryTargetType']['workoutTargetTypeKey']
        if secondary_target_type == 'pace.zone':
            secondary_target['min'] = timedelta(seconds=int(1000 / float(step_json['secondaryTargetValueOne']))
                                                ).total_seconds()
            secondary_target['max'] = timedelta(seconds=int(1000 / float(step_json['secondaryTargetValueTwo']))
                                                ).total_seconds()
            secondary_target['zone'] = step_json['secondaryZoneNumber']
        elif secondary_target_type == 'cadence':
            secondary_target['min'] = int(step_json.get('secondaryTargetValueOne', None))
            secondary_target['max'] = int(step_json.get('secondaryTargetValueTwo', None))
        elif secondary_target_type in ['heart.rate.zone', 'power.zone']:
            secondary_target['zone'] = str(step_json.get('secondaryZoneNumber', None))
            secondary_target['min'] = int(step_json.get('secondaryTargetValueOne', None))
            secondary_target['max'] = int(step_json.get('secondaryTargetValueTwo', None))
        elif secondary_target_type not in ['lap.button', 'no.target']:
            print(secondary_target_type)
            print(step)
    return step


@staticmethod
def weight_extraction(step_json, step) -> dict:
    weight_value: str | None = step_json.get('weightValue')
    weight_unit: str | None = step_json.get('weightUnit', {}).get('unitKey') if step_json.get('weightUnit') else None
    if weight_value is not None:
        if weight_unit == 'kilogram':
            step['weight'] = f"{weight_value}kg"
        elif weight_unit == 'pound':
            step['weight'] = f"{weight_value}pound"
    return step


@staticmethod
def step_extraction(step_json) -> dict | None:
    if step_json['stepType']['stepTypeKey'] != 'repeat':
        step: dict = {
            'type': step_json['stepType']['stepTypeKey'],
            'description': step_json.get('description', ''),
            'equipment': step_json.get('equipmentType', {}).get('equipmentTypeKey'),
            'category': step_json.get('category'),
            'exerciseName': step_json.get('exerciseName'),
            'repeatDuration': step_json.get('repeatDuration')
        }
        step = end_condition_extraction(step_json, step)
        step = target_extraction(step_json, step)
        step = secondary_target_extraction(step_json, step)
        step = weight_extraction(step_json, step)
        return step


@staticmethod
def workout_export_yaml(workout, filename) -> None:
    workout_dict: dict = {}
    workout_dict['name'] = workout.get('workoutName', '')
    workout_dict['sport'] = workout['sportType'].get('sportTypeKey', '')
    workout_dict['subsport'] = workout.get('subSportType', '') if 'subSportType' in workout else ''
    workout_dict['description'] = workout.get('description', '')
    workout_dict['steps'] = []

    if 'workoutSegments' in workout and workout['workoutSegments']:
        workout_segment = workout['workoutSegments'][0]
        workout_steps = workout_segment.get('workoutSteps', [])

        for step_json in workout_steps:
            step_type = step_json['stepType'].get('stepTypeKey', '')

            if step_type != 'repeat':
                workout_dict['steps'].append(step_extraction(step_json))
            else:
                if 'numberOfIterations' in step_json and step_json['numberOfIterations'] is not None:
                    rep_step = [step_extraction(rep_step_json) for rep_step_json in step_json.get('workoutSteps', [])]
                    for _ in range(step_json['numberOfIterations']):
                        workout_dict['steps'].extend(rep_step)
                else:
                    for rep_step_json in step_json.get('workoutSteps', []):
                        rep_step_json['repeatDuration'] = str(timedelta(seconds=int(
                            step_json.get('endConditionValue', 0))))
                        workout_dict['steps'].append(step_extraction(rep_step_json))

    else:
        print(filename)

    with open(filename, 'w') as file:
        try:
            yaml.dump(workout_dict, file, default_flow_style=None)
        except Exception as e:
            print(f"Error occurred while writing to file: {e}")


@staticmethod
def event_export_yaml(event, filename) -> None:
    try:
        with open(filename, 'w') as file:
            yaml.dump(event, file, default_flow_style=None)
    except Exception as e:
        # Handle any exception that may occur during file operation
        print(f"An error occurred: {e}")


@staticmethod
def note_export_yaml(note, filename) -> None:
    note_dict: dict = {
        'name': note.get('noteName', ''),
        'content': note.get('content', '')
    }
    try:
        with open(filename, 'w') as file:
            yaml.dump(note_dict, file, default_flow_style=None)
    except Exception as e:
        # Handle any exception that may occur during file operation
        print(f"An error occurred: {e}")
