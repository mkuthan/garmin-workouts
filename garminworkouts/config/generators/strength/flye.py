from garminworkouts.config.generators.strength.simple_step import exercise_generator


def cable_crossover_rep_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='CABLE_CROSSOVER',
        duration=duration,
        execution='reps')


def cable_crossover_hold_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='CABLE_CROSSOVER',
        duration=duration,
        execution='hold')


def decline_dumbbell_flye_rep_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='DECLINE_DUMBBELL_FLYE',
        duration=duration,
        execution='reps')


def decline_dumbbell_flye_hold_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='DECLINE_DUMBBELL_FLYE',
        duration=duration,
        execution='hold')


def dumbbell_flye_rep_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='DUMBBELL_FLYE',
        duration=duration,
        execution='reps')


def dumbbell_flye_hold_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='DUMBBELL_FLYE',
        duration=duration,
        execution='hold')


def incline_dumbbell_flye_rep_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='INCLINE_DUMBBELL_FLYE',
        duration=duration,
        execution='reps')


def incline_dumbbell_flye_hold_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='INCLINE_DUMBBELL_FLYE',
        duration=duration,
        execution='hold')


def incline_reverse_flye_rep_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='INCLINE_REVERSE_FLYE',
        duration=duration,
        execution='reps')


def incline_reverse_flye_hold_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='INCLINE_REVERSE_FLYE',
        duration=duration,
        execution='hold')


def kettlebell_flye_rep_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='KETTLEBELL_FLYE',
        duration=duration,
        execution='reps')


def kettlebell_flye_hold_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='KETTLEBELL_FLYE',
        duration=duration,
        execution='hold')


def kneeling_rear_flye_rep_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='KNEELING_REAR_FLYE',
        duration=duration,
        execution='reps')


def kneeling_rear_flye_hold_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='KNEELING_REAR_FLYE',
        duration=duration,
        execution='hold')


def single_arm_standing_cable_reverse_flye_rep_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='SINGLE_ARM_STANDING_CABLE_REVERSE_FLYE',
        duration=duration,
        execution='reps')


def single_arm_standing_cable_reverse_flye_hold_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='SINGLE_ARM_STANDING_CABLE_REVERSE_FLYE',
        duration=duration,
        execution='hold')


def swiss_ball_dumbbell_flye_rep_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='SWISS_BALL_DUMBBELL_FLYE',
        duration=duration,
        execution='reps')


def swiss_ball_dumbbell_flye_hold_generator(duration) -> dict:
    return exercise_generator(
        category='FLYE',
        exercise_name='SWISS_BALL_DUMBBELL_FLYE',
        duration=duration,
        execution='hold')
