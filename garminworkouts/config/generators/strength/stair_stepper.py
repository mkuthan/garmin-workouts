from garminworkouts.config.generators.strength.simple_step import exercise_generator


def stair_stepper_rep_generator(duration) -> dict:
    return exercise_generator(
        category='STAIR_STEPPER',
        exercise_name='STAIR_STEPPER',
        duration=duration,
        execution='reps')


def stair_stepper_hold_generator(duration) -> dict:
    return exercise_generator(
        category='STAIR_STEPPER',
        exercise_name='STAIR_STEPPER',
        duration=duration,
        execution='hold')
