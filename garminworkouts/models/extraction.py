from datetime import timedelta
import yaml


@staticmethod
def target_extraction(step_json, step):
    end_condition = step_json['endCondition']['conditionTypeKey']
    if end_condition == 'time':
        step['duration'] = str(timedelta(seconds=int(step_json['endConditionValue'])))
    elif end_condition == 'distance':
        step['duration'] = str(float(step_json['endConditionValue'])/1000) + 'km'
    elif end_condition == 'reps':
        step['duration'] = str(step_json['endConditionValue']) + 'reps'
    elif end_condition == 'heart.rate':
        step['duration'] = str(step_json['endConditionValue']) + 'ppm' + step_json['endConditionCompare']
    elif end_condition != 'lap.button':
        print(end_condition, step_json['endConditionValue'])
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
        step = {}
        step['type'] = step_json['stepType']['stepTypeKey']

        step = target_extraction(step_json, step)

        step['target'] = {}
        step['target']['type'] = 'no.target'
        if ('targetType' in step_json) and (step_json['targetType'] is not None):
            step['target']['type'] = step_json['targetType']['workoutTargetTypeKey']
            if step['target']['type'] == 'pace.zone':
                step['target']['min'] = str(timedelta(seconds=int(1000 / float(step_json['targetValueOne']))))[2:]
                step['target']['max'] = str(timedelta(seconds=int(1000 / float(step_json['targetValueTwo']))))[2:]
            elif step['target']['type'] == 'cadence' or step['target']['type'] == 'heart.rate.zone':
                step['target']['min'] = str(int(step_json['targetValueOne']))
                step['target']['max'] = str(int(step_json['targetValueTwo']))
            elif step['target']['type'] != 'lap.button' and step['target']['type'] != 'no.target':
                print(step['target']['type'])
                print(step)

        step['description'] = step_json['description'] if step_json['description'] else ''

        step = weight_extraction(step_json, step)

        if ('equipmentType' in step_json) and (
            step_json['equipmentType'] is not None) and (
             step_json['equipmentType']['equipmentTypeKey'] is not None):
            print(step_json['equipmentType'])
            step['equipment'] = step_json['equipmentType']['equipmentTypeKey']
        if ('category' in step_json) and (step_json['category'] is not None):
            step['category'] = step_json['category']
        if ('exerciseName' in step_json) and (step_json['exerciseName'] is not None):
            step['exerciseName'] = step_json['exerciseName']

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
                workout_dict["steps"].append(step_extraction(step_json))
            else:
                if ('numberOfIterations' in step_json) and (step_json['numberOfIterations'] is not None):
                    for j in range(step_json['numberOfIterations']):
                        for k in range(len(step_json['workoutSteps'])):
                            workout_dict["steps"].append(step_extraction(step_json['workoutSteps'][k]))
    else:
        print(filename)
    with open(filename, 'w') as file:
        yaml.dump(workout_dict, file)
