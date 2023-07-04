from datetime import timedelta
import yaml


@staticmethod
def end_condition_extraction(step_json, step):
    end_condition = step_json['endCondition']['conditionTypeKey']
    if end_condition == 'time' or end_condition == 'fixed.rest':
        step['duration'] = str(timedelta(seconds=int(step_json['endConditionValue'])))
    elif end_condition == 'distance':
        step['duration'] = str(round(float(step_json['endConditionValue'])/1000, 3)) + 'km'
    elif end_condition == 'reps':
        step['duration'] = str(int(step_json['endConditionValue'])) + 'reps'
    elif end_condition == 'heart.rate':
        step['duration'] = str(int(step_json['endConditionValue'])) + 'ppm' + step_json['endConditionCompare']
    elif end_condition != 'lap.button':
        print(end_condition, step_json['endConditionValue'])
    return step


@staticmethod
def target_extraction(step_json, step):
    step['target'] = {}
    step['target']['type'] = 'no.target'
    if ('targetType' in step_json) and (step_json['targetType'] is not None):
        step['target']['type'] = step_json['targetType']['workoutTargetTypeKey']
        if step['target']['type'] == 'pace.zone':
            step['target']['min'] = str(timedelta(seconds=int(1000 / float(step_json['targetValueOne']))))[2:]
            step['target']['max'] = str(timedelta(seconds=int(1000 / float(step_json['targetValueTwo']))))[2:]
        elif step['target']['type'] == 'cadence':
            step['target']['min'] = str(int(step_json['targetValueOne'])) if step_json['targetValueOne'] else None
            step['target']['max'] = str(int(step_json['targetValueTwo'])) if step_json['targetValueTwo'] else None
        elif step['target']['type'] == 'heart.rate.zone' or step['target']['type'] == 'power.zone':
            if step_json['zoneNumber']:
                step['target']['zone'] = str(step_json['zoneNumber'])
            else:
                step['target']['min'] = str(
                    int(step_json['targetValueOne'])) if step_json['targetValueOne'] else None
                step['target']['max'] = str(
                    int(step_json['targetValueTwo'])) if step_json['targetValueTwo'] else None
        elif step['target']['type'] != 'lap.button' and step['target']['type'] != 'no.target':
            print(step['target']['type'])
            print(step)

    return step


def secondary_target_extraction(step_json, step):
    if ('secondaryTargetType' in step_json) and (step_json['secondaryTargetType'] is not None):
        step['secondaryTarget'] = {}
        step['secondaryTarget']['type'] = step_json['secondaryTargetType']['workoutTargetTypeKey']
        if step['secondaryTarget']['type'] == 'pace.zone':
            step['secondaryTarget']['min'] = str(timedelta(seconds=int(1000 / float(
                step_json['secondaryTargetValueOne']))))[2:]
            step['secondaryTarget']['max'] = str(timedelta(seconds=int(1000 / float(
                step_json['secondaryTargetValueTwo']))))[2:]
            step['secondaryTarget']['zone'] = step_json['secondaryZoneNumber']
        elif step['secondaryTarget']['type'] == 'cadence':
            step['secondaryTarget']['min'] = str(int(step_json['secondaryTargetValueOne']))
            step['secondaryTarget']['max'] = str(int(step_json['secondaryTargetValueTwo'])) if step_json[
                'secondaryTargetValueTwo'] else None
        elif (step['secondaryTarget']['type'] == 'heart.rate.zone' or
              step['secondaryTarget']['type'] == 'power.zone'):
            if step_json['secondaryZoneNumber']:
                step['secondaryTarget']['zone'] = str(step_json['secondaryZoneNumber'])
            else:
                step['secondaryTarget']['min'] = str(int(step_json['secondaryTargetValueOne'])) if step_json[
                    'secondaryTargetValueOne'] else None
                step['secondaryTarget']['max'] = str(int(step_json['secondaryTargetValueTwo'])) if step_json[
                    'secondaryTargetValueTwo'] else None
        elif step['secondaryTarget']['type'] != 'lap.button' and step['secondaryTarget']['type'] != 'no.target':
            print(step['secondaryTarget']['type'])
            print(step)

    return step


@staticmethod
def weight_extraction(step_json, step):
    if ('weightValue' in step_json) and (step_json['weightValue'] is not None):
        if step_json['weightUnit']['unitKey'] == 'kilogram':
            step['weight'] = str(step_json['weightValue']) + 'kg'
        elif step_json['weightUnit']['unitKey'] == 'pound':
            step['weight'] = str(step_json['weightValue']) + 'pound'
        else:
            print(step_json['weightUnit']['unitKey'])
    return step


@staticmethod
def step_extraction(step_json):
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
def export_yaml(workout, filename):
    workout_dict = {}
    workout_dict['name'] = workout['workoutName']
    workout_dict['sport'] = workout['sportType']['sportTypeKey']
    workout_dict['description'] = workout['description'] if 'description' in workout else ''
    workout_dict['steps'] = []

    if len(workout['workoutSegments']) > 0:
        for i in range(len(workout['workoutSegments'][0]['workoutSteps'])):
            step_json = workout['workoutSegments'][0]['workoutSteps'][i]

            if step_json['stepType']['stepTypeKey'] != 'repeat':
                workout_dict['steps'].append(step_extraction(step_json))
            else:
                if ('numberOfIterations' in step_json) and (step_json['numberOfIterations'] is not None):
                    for j in range(step_json['numberOfIterations']):
                        for k in range(len(step_json['workoutSteps'])):
                            workout_dict['steps'].append(step_extraction(step_json['workoutSteps'][k]))
                else:
                    for k in range(len(step_json['workoutSteps'])):
                        step_json['workoutSteps'][k]['repeatDuration'] = str(
                            timedelta(seconds=int(step_json['endConditionValue'])))
                        workout_dict['steps'].append(step_extraction(step_json['workoutSteps'][k]))
    else:
        print(filename)
    with open(filename, 'w') as file:
        yaml.dump(workout_dict, file)
