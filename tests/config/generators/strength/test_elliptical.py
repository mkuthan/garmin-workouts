import pytest

from garminworkouts.config.generators.strength.elliptical import (
    elliptical_rep_generator,
    elliptical_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (elliptical_rep_generator, 'ELLIPTICAL', 'reps'),
    (elliptical_hold_generator, 'ELLIPTICAL', 'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'ELLIPTICAL'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
