import pytest
from garminworkouts.config.generators.strength.simple_step import exercise_generator, rest_generator
from garminworkouts.config.generators.running.simple_step import (
    R0_step_generator, R1_step_generator, R1p_step_generator, R2_step_generator,
    R3_step_generator, R3p_step_generator, R4_step_generator, R5_step_generator,
    R6_step_generator, recovery_step_generator, aerobic_step_generator,
    lt_step_generator, lr_step_generator, marathon_step_generator,
    hm_step_generator, tuneup_step_generator, warmup_step_generator,
    cooldown_step_generator, walk_step_generator
)


@pytest.mark.parametrize("generator, duration, expected", [
    (R0_step_generator, 10, {'type': 'interval', 'duration': 10, 'target': 'R0', 'description': 'R0 pace zone',
                             'category': None, 'exerciseName': None}),
    (R1_step_generator, 20, {'type': 'interval', 'duration': 20, 'target': 'R1', 'description': 'R1 pace zone',
                             'category': None, 'exerciseName': None}),
    (R1p_step_generator, 30, {'type': 'interval', 'duration': 30, 'target': 'R1p', 'description': 'R1+ pace zone',
                              'category': None, 'exerciseName': None}),
    (R3p_step_generator, 60, {'type': 'interval', 'duration': 60, 'target': 'R3p', 'description': 'R3+ pace zone',
                              'category': None, 'exerciseName': None}),
    (R4_step_generator, 70, {'type': 'interval', 'duration': 70, 'target': 'R4', 'description': 'R4 pace zone',
                             'category': None, 'exerciseName': None}),
    (R5_step_generator, 80, {'type': 'interval', 'duration': 80, 'target': 'R5', 'description': 'R5 pace zone',
                             'category': None, 'exerciseName': None}),
    (R6_step_generator, 90, {'type': 'interval', 'duration': 90, 'target': 'R6', 'description': 'R6 pace zone',
                             'category': None, 'exerciseName': None}),
    (walk_step_generator, 190,  {'type': 'rest', 'duration': 190, 'target': 'WALK', 'description': 'Walk',
                                 'category': None, 'exerciseName': None}),
    (tuneup_step_generator, 160,
     {'type': 'interval', 'duration': 160, 'target': '10KM_PACE', 'description': '10K pace run',
      'category': None, 'exerciseName': None}),
    (warmup_step_generator, 170,
     {'type': 'warmup', 'duration': 170, 'target': 'AEROBIC_HEART_RATE', 'description': 'Warm up',
      'category': None, 'exerciseName': None}),
])
def test_single_use_generators(generator, duration, expected):
    result = generator(duration)
    assert result == expected


@pytest.mark.parametrize("generator, duration, pace, expected", [
    (recovery_step_generator, 100, False,
     {'type': 'recovery', 'duration': 100, 'target': 'RECOVERY_HEART_RATE', 'description': 'Recovery pace',
      'category': None, 'exerciseName': None}),
    (aerobic_step_generator, 110,  False,
     {'type': 'interval', 'duration': 110, 'target': 'AEROBIC_HEART_RATE', 'description': 'Aerobic pace',
      'category': None, 'exerciseName': None}),
    (cooldown_step_generator, 180,  False,
     {'type': 'cooldown', 'duration': 180, 'target': 'AEROBIC_HEART_RATE', 'description': 'Cool down',
      'category': None, 'exerciseName': None}),
    (recovery_step_generator, 100, True,
     {'type': 'recovery', 'duration': 100, 'target': 'RECOVERY_PACE', 'description': 'Recovery pace',
      'category': None, 'exerciseName': None}),
    (aerobic_step_generator, 110,  True,
     {'type': 'interval', 'duration': 110, 'target': 'AEROBIC_PACE', 'description': 'Aerobic pace',
      'category': None, 'exerciseName': None}),
    (cooldown_step_generator, 180,  True,
     {'type': 'cooldown', 'duration': 180, 'target': 'AEROBIC_PACE', 'description': 'Cool down',
      'category': None, 'exerciseName': None}),
    (lr_step_generator, 240, False, {'type': 'interval', 'duration': 240, 'target': 'LONG_RUN_HEART_RATE',
                                     'description': 'Long run pace', 'category': None, 'exerciseName': None}),
    (lr_step_generator,  250, True, {'type': 'interval', 'duration': 250, 'target': 'LONG_RUN_PACE',
                                     'description': 'Long run pace', 'category': None, 'exerciseName': None}),
])
def test_pace_generators(generator, duration, pace, expected):
    result = generator(duration, pace)
    assert result == expected


@pytest.mark.parametrize("generator, duration, target, expected", [
    (marathon_step_generator, 200, '', {'type': 'interval', 'duration': 200, 'target': 'MARATHON_PACE',
                                        'description': 'Marathon pace', 'category': None, 'exerciseName': None}),
    (hm_step_generator, 210, '', {'type': 'interval', 'duration': 210, 'target': 'HALF_MARATHON_PACE',
                                  'description': 'Half Marathon pace', 'category': None, 'exerciseName': None}),
    (R2_step_generator, 40, '', {'type': 'interval', 'duration': 40, 'target': 'R2', 'description': 'R2 pace zone',
                                 'category': None, 'exerciseName': None}),
    (R3_step_generator, 50, '', {'type': 'interval', 'duration': 50, 'target': 'R3', 'description': 'R3 pace zone',
                                 'category': None, 'exerciseName': None}),
    ])
def test_target_duration_generators(generator, duration, target, expected):
    result = generator(duration, target)
    assert result == expected


@pytest.mark.parametrize("generator, duration, target, pace, expected", [
    (lt_step_generator, 220, '', False, {'type': 'interval', 'duration': 220, 'target': 'THRESHOLD_HEART_RATE',
                                         'description': 'Threshold pace', 'category': None, 'exerciseName': None}),
    (lt_step_generator, 230, '', True, {'type': 'interval', 'duration': 230, 'target': 'THRESHOLD_PACE',
                                        'description': 'Threshold pace', 'category': None, 'exerciseName': None}),

    ])
def test_lt_generators(generator, target, duration, pace, expected):
    if target is not None:
        result = generator(duration, target, pace)
    else:
        result = generator(duration, pace)
    assert result == expected


@pytest.mark.parametrize("category, exercise_name, duration, execution, expected", [
    ('PUSH_UP', 'PUSH_UP', '10', 'reps', {'type': 'interval', 'duration': '10reps',
     'target': 'NO_TARGET', 'description': 'Push Up', 'category': 'PUSH_UP', 'exerciseName': 'PUSH_UP'}),
    ('SQUAT', 'SQUAT', '20', 'hold', {'type': 'interval', 'duration': 'lap.button', 'target': 'NO_TARGET',
     'description': '20-count hold', 'category': 'SQUAT', 'exerciseName': 'SQUAT'}),
    ('PLANK', 'PLANK', '30', '', {'type': 'interval', 'duration': 'lap.button', 'target': 'NO_TARGET',
     'description': 'Max Planks', 'category': 'PLANK', 'exerciseName': 'PLANK'}),
    ])
def test_exercise_generator(category, exercise_name, duration, execution, expected):
    result = exercise_generator(category, exercise_name, duration, execution)
    assert result == expected


def test_exercise_generator_invalid_category():
    with pytest.raises(KeyError):
        exercise_generator('invalid_category', 'push_up', '10', 'reps')


def test_exercise_generator_invalid_exercise():
    with pytest.raises(ValueError):
        exercise_generator('CORE', 'invalid_exercise', '10', 'reps')


@pytest.mark.parametrize("duration, expected", [
    ('10s', {'type': 'rest', 'duration': '10s', 'target': 'NO_TARGET',
     'description': '', 'category': None, 'exerciseName': None}),
    ('20s', {'type': 'rest', 'duration': '20s', 'target': 'NO_TARGET',
     'description': '', 'category': None, 'exerciseName': None}),
])
def test_rest_generator(duration, expected):
    result = rest_generator(duration)
    assert result == expected
