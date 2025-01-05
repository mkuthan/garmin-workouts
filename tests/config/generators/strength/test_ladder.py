import pytest

from garminworkouts.config.generators.strength.ladder import (
    agility_rep_generator,
    agility_hold_generator,
    speed_rep_generator,
    speed_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (agility_rep_generator,
     'AGILITY',
     'reps'),
    (agility_hold_generator,
     'AGILITY',
     'hold'),
    (speed_rep_generator,
     'SPEED',
     'reps'),
    (speed_hold_generator,
     'SPEED',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'LADDER'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
