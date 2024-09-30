from garminworkouts.config.generators.strength.simple_step import exercise_generator


def indoor_track_run_rep_generator(duration) -> dict:
    return exercise_generator(
        category='RUN_INDOOR',
        exercise_name='INDOOR_TRACK_RUN',
        duration=duration,
        execution='reps')


def indoor_track_run_hold_generator(duration) -> dict:
    return exercise_generator(
        category='RUN_INDOOR',
        exercise_name='INDOOR_TRACK_RUN',
        duration=duration,
        execution='hold')


def treadmill_rep_generator(duration) -> dict:
    return exercise_generator(
        category='RUN_INDOOR',
        exercise_name='TREADMILL',
        duration=duration,
        execution='reps')


def treadmill_hold_generator(duration) -> dict:
    return exercise_generator(
        category='RUN_INDOOR',
        exercise_name='TREADMILL',
        duration=duration,
        execution='hold')
