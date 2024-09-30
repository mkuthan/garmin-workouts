from garminworkouts.config.generators.strength.simple_step import exercise_generator


def lateral_swing_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SLEDGE_HAMMER',
        exercise_name='LATERAL_SWING',
        duration=duration,
        execution='reps')


def lateral_swing_hold_generator(duration) -> dict:
    return exercise_generator(
        category='SLEDGE_HAMMER',
        exercise_name='LATERAL_SWING',
        duration=duration,
        execution='hold')


def hammer_slam_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SLEDGE_HAMMER',
        exercise_name='HAMMER_SLAM',
        duration=duration,
        execution='reps')


def hammer_slam_hold_generator(duration) -> dict:
    return exercise_generator(
        category='SLEDGE_HAMMER',
        exercise_name='HAMMER_SLAM',
        duration=duration,
        execution='hold')


def sledge_hammer_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SLEDGE_HAMMER',
        exercise_name='SLEDGE_HAMMER',
        duration=duration,
        execution='reps')


def sledge_hammer_hold_generator(duration) -> dict:
    return exercise_generator(
        category='SLEDGE_HAMMER',
        exercise_name='SLEDGE_HAMMER',
        duration=duration,
        execution='hold')
