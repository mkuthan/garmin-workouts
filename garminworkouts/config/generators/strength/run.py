from garminworkouts.config.generators.strength.simple_step import exercise_generator


def jog_rep_generator(duration) -> dict:
    return exercise_generator(
        category='RUN',
        exercise_name='JOG',
        duration=duration,
        execution='reps')


def jog_hold_generator(duration) -> dict:
    return exercise_generator(
        category='RUN',
        exercise_name='JOG',
        duration=duration,
        execution='hold')


def run_rep_generator(duration) -> dict:
    return exercise_generator(
        category='RUN',
        exercise_name='RUN',
        duration=duration,
        execution='reps')


def run_hold_generator(duration) -> dict:
    return exercise_generator(
        category='RUN',
        exercise_name='RUN',
        duration=duration,
        execution='hold')


def run_or_walk_rep_generator(duration) -> dict:
    return exercise_generator(
        category='RUN',
        exercise_name='RUN_OR_WALK',
        duration=duration,
        execution='reps')


def run_or_walk_hold_generator(duration) -> dict:
    return exercise_generator(
        category='RUN',
        exercise_name='RUN_OR_WALK',
        duration=duration,
        execution='hold')


def sprint_rep_generator(duration) -> dict:
    return exercise_generator(
        category='RUN',
        exercise_name='SPRINT',
        duration=duration,
        execution='reps')


def sprint_hold_generator(duration) -> dict:
    return exercise_generator(
        category='RUN',
        exercise_name='SPRINT',
        duration=duration,
        execution='hold')


def walk_rep_generator(duration) -> dict:
    return exercise_generator(
        category='RUN',
        exercise_name='WALK',
        duration=duration,
        execution='reps')


def walk_hold_generator(duration) -> dict:
    return exercise_generator(
        category='RUN',
        exercise_name='WALK',
        duration=duration,
        execution='hold')
