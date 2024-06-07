from datetime import timedelta
import yaml


@staticmethod
def end_condition_extraction(step_json, step) -> dict:
    end_condition: str = step_json['endCondition']['conditionTypeKey']
    if end_condition == 'time' or end_condition == 'fixed.rest':
        step['duration'] = str(timedelta(seconds=int(step_json['endConditionValue'])))
    elif end_condition == 'distance':
        step['duration'] = str(round(float(step_json['endConditionValue']) / 1000, 3)) + 'km'
    elif end_condition == 'reps':
        step['duration'] = str(int(step_json['endConditionValue'])) + 'reps'
    elif end_condition == 'heart.rate':
        step['duration'] = str(int(step_json['endConditionValue'])) + 'ppm' + step_json['endConditionCompare']
    elif end_condition != 'lap.button':
        step['duration'] = 'lap.button'
    return step


@staticmethod
def target_extraction(step_json, step) -> dict:
    step['target'] = {}
    step['target']['type'] = 'no.target'

    if 'targetType' in step_json and step_json['targetType']:
        target_type_key: dict = step_json['targetType']['workoutTargetTypeKey']
        step['target']['type'] = target_type_key

        if target_type_key == 'pace.zone':
            step['target']['min'] = str(timedelta(seconds=int(1000 / float(step_json['targetValueOne']))))[2:]
            step['target']['max'] = str(timedelta(seconds=int(1000 / float(step_json['targetValueTwo']))))[2:]
        elif target_type_key == 'cadence':
            step['target']['min'] = str(int(step_json['targetValueOne'])) if step_json['targetValueOne'] else None
            step['target']['max'] = str(int(step_json['targetValueTwo'])) if step_json['targetValueTwo'] else None
        elif target_type_key in ['heart.rate.zone', 'power.zone']:
            if step_json.get('zoneNumber'):
                step['target']['zone'] = str(step_json['zoneNumber'])
            else:
                step['target']['min'] = str(int(step_json['targetValueOne'])) if step_json['targetValueOne'] else None
                step['target']['max'] = str(int(step_json['targetValueTwo'])) if step_json['targetValueTwo'] else None
        elif target_type_key not in ['lap.button', 'no.target']:
            print(target_type_key)
            print(step)

    return step


def secondary_target_extraction(step_json, step) -> dict:
    if ('secondaryTargetType' in step_json) and (step_json['secondaryTargetType'] is not None):
        secondary_target = step['secondaryTarget'] = {}
        secondary_target_type = step_json['secondaryTargetType']['workoutTargetTypeKey']

        if secondary_target_type == 'pace.zone':
            secondary_target['min'] = timedelta(seconds=int(1000 / float(step_json['secondaryTargetValueOne']))
                                                ).total_seconds()
            secondary_target['max'] = timedelta(seconds=int(1000 / float(step_json['secondaryTargetValueTwo']))
                                                ).total_seconds()
            secondary_target['zone'] = step_json['secondaryZoneNumber']

        elif secondary_target_type == 'cadence':
            secondary_target['min'] = int(step_json['secondaryTargetValueOne'])
            secondary_target['max'] = int(step_json['secondaryTargetValueTwo']) if step_json.get(

                'secondaryTargetValueTwo') else None

        elif secondary_target_type in ['heart.rate.zone', 'power.zone']:
            if step_json.get('secondaryZoneNumber'):
                secondary_target['zone'] = str(step_json['secondaryZoneNumber'])
            else:
                secondary_target['min'] = int(step_json['secondaryTargetValueOne']) if step_json.get(
                    'secondaryTargetValueOne') else None
                secondary_target['max'] = int(step_json['secondaryTargetValueTwo']) if step_json.get(
                    'secondaryTargetValueTwo') else None

        elif secondary_target_type not in ['lap.button', 'no.target']:
            print(secondary_target_type)
            print(step)

    return step


@staticmethod
def weight_extraction(step_json, step) -> dict:
    weight_value: str = step_json.get('weightValue')
    weight_unit: str = step_json.get('weightUnit', {}).get('unitKey')

    if weight_value is not None:
        if weight_unit == 'kilogram':
            step['weight'] = str(weight_value) + 'kg'
        elif weight_unit == 'pound':
            step['weight'] = str(weight_value) + 'pound'
        else:
            print(weight_unit)
    return step


@staticmethod
def step_extraction(step_json) -> dict | None:
    if step_json['stepType']['stepTypeKey'] != 'repeat':
        step: dict = {}
        step['type'] = step_json['stepType']['stepTypeKey']

        step = end_condition_extraction(step_json, step)
        step = target_extraction(step_json, step)
        step = secondary_target_extraction(step_json, step)

        step['description'] = step_json['description'] if step_json['description'] else ''

        step = weight_extraction(step_json, step)

        if ('equipmentType' in step_json) and (
            step_json['equipmentType'] is not None) and (
             step_json['equipmentType']['equipmentTypeKey'] is not None):
            step['equipment'] = step_json['equipmentType']['equipmentTypeKey']
        if ('category' in step_json) and (step_json['category'] is not None):
            step['category'] = step_json['category']
        if ('exerciseName' in step_json) and (step_json['exerciseName'] is not None):
            step['exerciseName'] = step_json['exerciseName']
        if ('repeatDuration' in step_json) and (step_json['repeatDuration'] is not None):
            step['repeatDuration'] = step_json['repeatDuration']

        return step


@staticmethod
def workout_export_yaml(workout, filename) -> None:
    workout_dict: dict = {}
    workout_dict['name'] = workout['workoutName']
    workout_dict['sport'] = workout['sportType']['sportTypeKey']
    if 'subSportType' in workout and workout['subSportType']:
        workout_dict['subsport'] = workout['subSportType']
    workout_dict['description'] = workout['description'] if 'description' in workout else ''
    workout_dict['steps'] = []

    if len(workout['workoutSegments']) > 0:
        for i in range(len(workout['workoutSegments'][0]['workoutSteps'])):
            step_json = workout['workoutSegments'][0]['workoutSteps'][i]

            if step_json['stepType']['stepTypeKey'] != 'repeat':
                workout_dict['steps'].append(step_extraction(step_json))
            else:
                if ('numberOfIterations' in step_json) and (step_json['numberOfIterations'] is not None):
                    rep_step = []
                    for k in range(len(step_json['workoutSteps'])):
                        rep_step.append(step_extraction(step_json['workoutSteps'][k]))
                    for j in range(step_json['numberOfIterations']):
                        workout_dict['steps'].append(rep_step)
                else:
                    for k in range(len(step_json['workoutSteps'])):
                        step_json['workoutSteps'][k]['repeatDuration'] = str(
                            timedelta(seconds=int(step_json['endConditionValue'])))
                        workout_dict['steps'].append(step_extraction(step_json['workoutSteps'][k]))
    else:
        print(filename)
    with open(filename, 'w') as file:
        yaml.dump(workout_dict, file, default_flow_style=None)


@staticmethod
def event_export_yaml(event, filename) -> None:
    try:
        with open(filename, 'w') as file:
            yaml.dump(event, file, default_flow_style=None)
    except FileNotFoundError:
        with open(filename.replace('/', ' '), 'w') as file:
            yaml.dump(event, file, default_flow_style=None)
    except OSError:
        with open(filename.replace('"', ''), 'w') as file:
            yaml.dump(event, file, default_flow_style=None)


@staticmethod
def note_export_yaml(note, filename) -> None:
    note_dict: dict = {}
    note_dict['name'] = note['noteName']
    note_dict['content'] = note['content']

    with open(filename, 'w') as file:
        yaml.dump(note_dict, file, default_flow_style=None)
