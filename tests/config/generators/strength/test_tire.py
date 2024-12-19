import pytest

from garminworkouts.config.generators.strength.tire import (
    flip_rep_generator,
    flip_hold_generator,
    tire_rep_generator,
    tire_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (flip_rep_generator, 'FLIP', 'reps'),
    (flip_hold_generator, 'FLIP', 'hold'),
    (tire_rep_generator, 'TIRE', 'reps'),
    (tire_hold_generator, 'TIRE', 'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'TIRE'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
