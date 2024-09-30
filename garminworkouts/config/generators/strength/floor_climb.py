from garminworkouts.config.generators.strength.simple_step import exercise_generator


def floor_climb_rep_generator(duration) -> dict:
    return exercise_generator(
        category='FLOOR_CLIMB',
        exercise_name='FLOOR_CLIMB',
        duration=duration,
        execution='reps')


def floor_climb_hold_generator(duration) -> dict:
    return exercise_generator(
        category='FLOOR_CLIMB',
        exercise_name='FLOOR_CLIMB',
        duration=duration,
        execution='hold')
