import pytest

from garminworkouts.config.generators.strength.run import (
    jog_rep_generator,
    jog_hold_generator,
    run_rep_generator,
    run_hold_generator,
    run_or_walk_rep_generator,
    run_or_walk_hold_generator,
    sprint_rep_generator,
    sprint_hold_generator,
    walk_rep_generator,
    walk_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (jog_rep_generator,
     'JOG',
     'reps'),
    (jog_hold_generator,
     'JOG',
     'hold'),
    (run_rep_generator,
     'RUN',
     'reps'),
    (run_hold_generator,
     'RUN',
     'hold'),
    (run_or_walk_rep_generator,
     'RUN_OR_WALK',
     'reps'),
    (run_or_walk_hold_generator,
     'RUN_OR_WALK',
     'hold'),
    (sprint_rep_generator,
     'SPRINT',
     'reps'),
    (sprint_hold_generator,
     'SPRINT',
     'hold'),
    (walk_rep_generator,
     'WALK',
     'reps'),
    (walk_hold_generator,
     'WALK',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'RUN'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
