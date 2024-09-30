from garminworkouts.config.generators.strength.simple_step import exercise_generator


def air_bike_rep_generator(duration) -> dict:
    return exercise_generator(
        category='INDOOR_BIKE',
        exercise_name='AIR_BIKE',
        duration=duration,
        execution='reps')


def air_bike_hold_generator(duration) -> dict:
    return exercise_generator(
        category='INDOOR_BIKE',
        exercise_name='AIR_BIKE',
        duration=duration,
        execution='hold')


def assault_bike_rep_generator(duration) -> dict:
    return exercise_generator(
        category='INDOOR_BIKE',
        exercise_name='ASSAULT_BIKE',
        duration=duration,
        execution='reps')


def assault_bike_hold_generator(duration) -> dict:
    return exercise_generator(
        category='INDOOR_BIKE',
        exercise_name='ASSAULT_BIKE',
        duration=duration,
        execution='hold')


def stationary_bike_rep_generator(duration) -> dict:
    return exercise_generator(
        category='INDOOR_BIKE',
        exercise_name='STATIONARY_BIKE',
        duration=duration,
        execution='reps')


def stationary_bike_hold_generator(duration) -> dict:
    return exercise_generator(
        category='INDOOR_BIKE',
        exercise_name='STATIONARY_BIKE',
        duration=duration,
        execution='hold')
