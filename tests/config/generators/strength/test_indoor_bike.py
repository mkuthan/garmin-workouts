import pytest

from garminworkouts.config.generators.strength.indoor_bike import (
    air_bike_rep_generator,
    air_bike_hold_generator,
    assault_bike_rep_generator,
    assault_bike_hold_generator,
    stationary_bike_rep_generator,
    stationary_bike_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (air_bike_rep_generator,
     'AIR_BIKE',
     'reps'),
    (air_bike_hold_generator,
     'AIR_BIKE',
     'hold'),
    (assault_bike_rep_generator,
     'ASSAULT_BIKE',
     'reps'),
    (assault_bike_hold_generator,
     'ASSAULT_BIKE',
     'hold'),
    (stationary_bike_rep_generator,
     'STATIONARY_BIKE',
     'reps'),
    (stationary_bike_hold_generator,
     'STATIONARY_BIKE',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'INDOOR_BIKE'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
