import pytest

from garminworkouts.config.generators.strength.floor_climb import (
    floor_climb_rep_generator,
    floor_climb_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (floor_climb_rep_generator,
     'FLOOR_CLIMB',
     'reps'),
    (floor_climb_hold_generator,
     'FLOOR_CLIMB',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'FLOOR_CLIMB'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
