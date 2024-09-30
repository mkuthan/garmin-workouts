from garminworkouts.config.generators.strength.simple_step import exercise_generator


def agility_rep_generator(duration) -> dict:
    return exercise_generator(
        category='LADDER',
        exercise_name='AGILITY',
        duration=duration,
        execution='reps')


def agility_hold_generator(duration) -> dict:
    return exercise_generator(
        category='LADDER',
        exercise_name='AGILITY',
        duration=duration,
        execution='hold')


def speed_rep_generator(duration) -> dict:
    return exercise_generator(
        category='LADDER',
        exercise_name='SPEED',
        duration=duration,
        execution='reps')


def speed_hold_generator(duration) -> dict:
    return exercise_generator(
        category='LADDER',
        exercise_name='SPEED',
        duration=duration,
        execution='hold')
