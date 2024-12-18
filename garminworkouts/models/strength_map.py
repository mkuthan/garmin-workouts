import os
from garminworkouts.models.strength import (BANDED_EXERCISES, BATTLE_ROPE, BENCH_PRESS, BIKE_OUTDOOR, CALF_RAISE,
                                            CARDIO, CARRY, CHOP, CORE, CRUNCH, CURL, DEADLIFT, ELLIPTICAL, FLOOR_CLIMB,
                                            FLYE, HIP_RAISE, HIP_STABILITY, HIP_SWING, HYPEREXTENSION, INDOOR_BIKE,
                                            LADDER, LATERAL_RAISE, LEG_CURL, LEG_RAISE, LUNGE, OLYMPIC_LIFT, PLANK,
                                            PLYO, PULL_UP, PUSH_UP, ROW, RUN, RUN_INDOOR, SANDBAG, SHOULDER_PRESS,
                                            SHOULDER_STABILITY, SHRUG, SIT_UP, SLED, SLEDGE_HAMMER, SQUAT,
                                            STAIR_STEPPER, SUSPENSION, TIRE, TOTAL_BODY, TRICEPS_EXTENSION, WARM_UP)


MAP = {
    'BANDED_EXERCISES': BANDED_EXERCISES,
    'BATTLE_ROPE': BATTLE_ROPE,
    'BENCH_PRESS': BENCH_PRESS,
    'BIKE_OUTDOOR': BIKE_OUTDOOR,
    'CALF_RAISE': CALF_RAISE,
    'CARDIO': CARDIO,
    'CARRY': CARRY,
    'CHOP': CHOP,
    'CORE': CORE,
    'CRUNCH': CRUNCH,
    'CURL': CURL,
    'DEADLIFT': DEADLIFT,
    'ELLIPTICAL': ELLIPTICAL,
    'FLOOR_CLIMB': FLOOR_CLIMB,
    'FLYE': FLYE,
    'HIP_RAISE': HIP_RAISE,
    'HIP_STABILITY': HIP_STABILITY,
    'HIP_SWING': HIP_SWING,
    'HYPEREXTENSION': HYPEREXTENSION,
    'INDOOR_BIKE': INDOOR_BIKE,
    'LADDER': LADDER,
    'LATERAL_RAISE': LATERAL_RAISE,
    'LEG_CURL': LEG_CURL,
    'LEG_RAISE': LEG_RAISE,
    'LUNGE': LUNGE,
    'OLYMPIC_LIFT': OLYMPIC_LIFT,
    'PLANK': PLANK,
    'PLYO': PLYO,
    'PULL_UP': PULL_UP,
    'PUSH_UP': PUSH_UP,
    'ROW': ROW,
    'RUN': RUN,
    'RUN_INDOOR': RUN_INDOOR,
    'SANDBAG': SANDBAG,
    'SHOULDER_PRESS': SHOULDER_PRESS,
    'SHOULDER_STABILITY': SHOULDER_STABILITY,
    'SHRUG': SHRUG,
    'SIT_UP': SIT_UP,
    'SLED': SLED,
    'SLEDGE_HAMMER': SLEDGE_HAMMER,
    'SQUAT': SQUAT,
    'STAIR_STEPPER': STAIR_STEPPER,
    'SUSPENSION': SUSPENSION,
    'TIRE': TIRE,
    'TOTAL_BODY': TOTAL_BODY,
    'TRICEPS_EXTENSION': TRICEPS_EXTENSION,
    'WARM_UP': WARM_UP,
}


def generate_functions(_list, _exercises):
    functions = []
    for exercise_name in _exercises.keys():
        function_name_rep = exercise_name.lower() + '_rep_generator'
        function_name_hold = exercise_name.lower() + '_hold_generator'
        function_code = f"""

def {function_name_rep}(duration) -> dict:
    return exercise_generator(
        category='{_list}',
        exercise_name='{exercise_name}',
        duration=duration,
        execution='reps')


def {function_name_hold}(duration) -> dict:
    return exercise_generator(
        category='{_list}',
        exercise_name='{exercise_name}',
        duration=duration,
        execution='hold')
"""
        functions.append(function_code)
    return functions

# Write the generated functions to a file


def write_functions_to_file(functions, output_file_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w') as file:
        file.write("from garminworkouts.config.generators.strength.simple_step import exercise_generator\n")
        for function in functions:
            file.write(function)


def write_test_functions_to_file(exercises, exercise_list, output_file_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w') as file:
        file.write("import pytest\n\n")
        file.write(f"from garminworkouts.config.generators.strength.{exercises.lower()} import (\n    ")
        for exercise_name in exercise_list.keys():
            function_name_rep = exercise_name.lower() + '_rep_generator'
            function_name_hold = exercise_name.lower() + '_hold_generator'
            file.write(function_name_rep)
            file.write(",\n    ")
            file.write(function_name_hold)
            file.write(",\n    ")
        file.write(")\n\n\n")
        file.write("@pytest.mark.parametrize(\"generator, exercise_name, execution\", [\n    ")
        for exercise_name in exercise_list.keys():
            function_name_rep = exercise_name.lower() + '_rep_generator'
            function_name_hold = exercise_name.lower() + '_hold_generator'
            file.write(f"({function_name_rep}, '{exercise_name}', 'reps'),\n    ")
            file.write(f"({function_name_hold}, '{exercise_name}', 'hold'),\n    ")
        file.write("])\n")
        d = 10
        file.write(f"""def test_exercise_generators(generator, exercise_name, execution):
    duration = "{d}reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "{d}-count hold"
    result = generator({d})
    assert result['category'] == '{exercises}'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
""")
