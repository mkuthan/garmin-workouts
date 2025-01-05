import pytest

from garminworkouts.config.generators.strength.sledge_hammer import (
    lateral_swing_rep_generator,
    lateral_swing_hold_generator,
    hammer_slam_rep_generator,
    hammer_slam_hold_generator,
    sledge_hammer_rep_generator,
    sledge_hammer_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (lateral_swing_rep_generator,
     'LATERAL_SWING',
     'reps'),
    (lateral_swing_hold_generator,
     'LATERAL_SWING',
     'hold'),
    (hammer_slam_rep_generator,
     'HAMMER_SLAM',
     'reps'),
    (hammer_slam_hold_generator,
     'HAMMER_SLAM',
     'hold'),
    (sledge_hammer_rep_generator,
     'SLEDGE_HAMMER',
     'reps'),
    (sledge_hammer_hold_generator,
     'SLEDGE_HAMMER',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'SLEDGE_HAMMER'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
