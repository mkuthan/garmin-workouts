from garminworkouts.config.generators.strength.simple_step import exercise_generator


def bike_rep_generator(duration) -> dict:
    return exercise_generator(
        category='BIKE_OUTDOOR',
        exercise_name='BIKE',
        duration=duration,
        execution='reps')


def bike_hold_generator(duration) -> dict:
    return exercise_generator(
        category='BIKE_OUTDOOR',
        exercise_name='BIKE',
        duration=duration,
        execution='hold')
