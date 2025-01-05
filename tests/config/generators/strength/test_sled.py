import pytest

from garminworkouts.config.generators.strength.sled import (
    backward_drag_rep_generator,
    backward_drag_hold_generator,
    chest_press_rep_generator,
    chest_press_hold_generator,
    forward_drag_rep_generator,
    forward_drag_hold_generator,
    low_push_rep_generator,
    low_push_hold_generator,
    push_rep_generator,
    push_hold_generator,
    row_rep_generator,
    row_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (backward_drag_rep_generator,
     'BACKWARD_DRAG',
     'reps'),
    (backward_drag_hold_generator,
     'BACKWARD_DRAG',
     'hold'),
    (chest_press_rep_generator,
     'CHEST_PRESS',
     'reps'),
    (chest_press_hold_generator,
     'CHEST_PRESS',
     'hold'),
    (forward_drag_rep_generator,
     'FORWARD_DRAG',
     'reps'),
    (forward_drag_hold_generator,
     'FORWARD_DRAG',
     'hold'),
    (low_push_rep_generator,
     'LOW_PUSH',
     'reps'),
    (low_push_hold_generator,
     'LOW_PUSH',
     'hold'),
    (push_rep_generator,
     'PUSH',
     'reps'),
    (push_hold_generator,
     'PUSH',
     'hold'),
    (row_rep_generator,
     'ROW',
     'reps'),
    (row_hold_generator,
     'ROW',
     'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'SLED'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
