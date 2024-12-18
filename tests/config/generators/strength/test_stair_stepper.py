import pytest

from garminworkouts.config.generators.strength.stair_stepper import (
    stair_stepper_rep_generator,
    stair_stepper_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (stair_stepper_rep_generator, 'STAIR_STEPPER', 'reps'),
    (stair_stepper_hold_generator, 'STAIR_STEPPER', 'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'STAIR_STEPPER'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
