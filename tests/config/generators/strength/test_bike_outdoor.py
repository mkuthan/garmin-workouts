import pytest

from garminworkouts.config.generators.strength.bike_outdoor import (
    bike_rep_generator,
    bike_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (bike_rep_generator,
     'BIKE',
     'reps'),
    (bike_hold_generator,
     'BIKE',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'BIKE_OUTDOOR'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
