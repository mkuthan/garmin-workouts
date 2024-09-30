from garminworkouts.config.generators.strength.simple_step import exercise_generator


def elliptical_rep_generator(duration) -> dict:
    return exercise_generator(
        category='ELLIPTICAL',
        exercise_name='ELLIPTICAL',
        duration=duration,
        execution='reps')


def elliptical_hold_generator(duration) -> dict:
    return exercise_generator(
        category='ELLIPTICAL',
        exercise_name='ELLIPTICAL',
        duration=duration,
        execution='hold')
