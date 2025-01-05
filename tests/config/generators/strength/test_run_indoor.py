import pytest

from garminworkouts.config.generators.strength.run_indoor import (
    indoor_track_run_rep_generator,
    indoor_track_run_hold_generator,
    treadmill_rep_generator,
    treadmill_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (indoor_track_run_rep_generator,
     'INDOOR_TRACK_RUN',
     'reps'),
    (indoor_track_run_hold_generator,
     'INDOOR_TRACK_RUN',
     'hold'),
    (treadmill_rep_generator,
     'TREADMILL',
     'reps'),
    (treadmill_hold_generator,
     'TREADMILL',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'RUN_INDOOR'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
