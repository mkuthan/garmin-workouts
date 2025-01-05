import pytest

from garminworkouts.config.generators.strength.hip_swing import (
    hip_swing_rep_generator,
    hip_swing_hold_generator,
    one_arm_swing_rep_generator,
    one_arm_swing_hold_generator,
    single_arm_dumbbell_swing_rep_generator,
    single_arm_dumbbell_swing_hold_generator,
    single_arm_kettlebell_swing_rep_generator,
    single_arm_kettlebell_swing_hold_generator,
    step_out_swing_rep_generator,
    step_out_swing_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (hip_swing_rep_generator,
     'HIP_SWING',
     'reps'),
    (hip_swing_hold_generator,
     'HIP_SWING',
     'hold'),
    (one_arm_swing_rep_generator,
     'ONE_ARM_SWING',
     'reps'),
    (one_arm_swing_hold_generator,
     'ONE_ARM_SWING',
     'hold'),
    (single_arm_dumbbell_swing_rep_generator,
     'SINGLE_ARM_DUMBBELL_SWING',
     'reps'),
    (single_arm_dumbbell_swing_hold_generator,
     'SINGLE_ARM_DUMBBELL_SWING',
     'hold'),
    (single_arm_kettlebell_swing_rep_generator,
     'SINGLE_ARM_KETTLEBELL_SWING',
     'reps'),
    (single_arm_kettlebell_swing_hold_generator,
     'SINGLE_ARM_KETTLEBELL_SWING',
     'hold'),
    (step_out_swing_rep_generator,
     'STEP_OUT_SWING',
     'reps'),
    (step_out_swing_hold_generator,
     'STEP_OUT_SWING',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'HIP_SWING'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
