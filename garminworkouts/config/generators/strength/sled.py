from garminworkouts.config.generators.strength.simple_step import exercise_generator


def backward_drag_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='BACKWARD_DRAG',
        duration=duration,
        execution='reps')


def backward_drag_hold_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='BACKWARD_DRAG',
        duration=duration,
        execution='hold')


def chest_press_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='CHEST_PRESS',
        duration=duration,
        execution='reps')


def chest_press_hold_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='CHEST_PRESS',
        duration=duration,
        execution='hold')


def forward_drag_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='FORWARD_DRAG',
        duration=duration,
        execution='reps')


def forward_drag_hold_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='FORWARD_DRAG',
        duration=duration,
        execution='hold')


def low_push_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='LOW_PUSH',
        duration=duration,
        execution='reps')


def low_push_hold_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='LOW_PUSH',
        duration=duration,
        execution='hold')


def push_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='PUSH',
        duration=duration,
        execution='reps')


def push_hold_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='PUSH',
        duration=duration,
        execution='hold')


def row_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='ROW',
        duration=duration,
        execution='reps')


def row_hold_generator(duration) -> dict:
    return exercise_generator(
        category='SLED',
        exercise_name='ROW',
        duration=duration,
        execution='hold')
