from garminworkouts.config.generators.strength.simple_step import exercise_generator


def flip_rep_generator(duration) -> dict:
    return exercise_generator(
        category='TIRE',
        exercise_name='FLIP',
        duration=duration,
        execution='reps')


def flip_hold_generator(duration) -> dict:
    return exercise_generator(
        category='TIRE',
        exercise_name='FLIP',
        duration=duration,
        execution='hold')


def tire_rep_generator(duration) -> dict:
    return exercise_generator(
        category='TIRE',
        exercise_name='TIRE',
        duration=duration,
        execution='reps')


def tire_hold_generator(duration) -> dict:
    return exercise_generator(
        category='TIRE',
        exercise_name='TIRE',
        duration=duration,
        execution='hold')
