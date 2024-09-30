from garminworkouts.config.generators.strength.simple_step import exercise_generator


def hip_swing_rep_generator(duration) -> dict:
    return exercise_generator(
        category='HIP_SWING',
        exercise_name='HIP_SWING',
        duration=duration,
        execution='reps')


def hip_swing_hold_generator(duration) -> dict:
    return exercise_generator(
        category='HIP_SWING',
        exercise_name='HIP_SWING',
        duration=duration,
        execution='hold')


def one_arm_swing_rep_generator(duration) -> dict:
    return exercise_generator(
        category='HIP_SWING',
        exercise_name='ONE_ARM_SWING',
        duration=duration,
        execution='reps')


def one_arm_swing_hold_generator(duration) -> dict:
    return exercise_generator(
        category='HIP_SWING',
        exercise_name='ONE_ARM_SWING',
        duration=duration,
        execution='hold')


def single_arm_dumbbell_swing_rep_generator(duration) -> dict:
    return exercise_generator(
        category='HIP_SWING',
        exercise_name='SINGLE_ARM_DUMBBELL_SWING',
        duration=duration,
        execution='reps')


def single_arm_dumbbell_swing_hold_generator(duration) -> dict:
    return exercise_generator(
        category='HIP_SWING',
        exercise_name='SINGLE_ARM_DUMBBELL_SWING',
        duration=duration,
        execution='hold')


def single_arm_kettlebell_swing_rep_generator(duration) -> dict:
    return exercise_generator(
        category='HIP_SWING',
        exercise_name='SINGLE_ARM_KETTLEBELL_SWING',
        duration=duration,
        execution='reps')


def single_arm_kettlebell_swing_hold_generator(duration) -> dict:
    return exercise_generator(
        category='HIP_SWING',
        exercise_name='SINGLE_ARM_KETTLEBELL_SWING',
        duration=duration,
        execution='hold')


def step_out_swing_rep_generator(duration) -> dict:
    return exercise_generator(
        category='HIP_SWING',
        exercise_name='STEP_OUT_SWING',
        duration=duration,
        execution='reps')


def step_out_swing_hold_generator(duration) -> dict:
    return exercise_generator(
        category='HIP_SWING',
        exercise_name='STEP_OUT_SWING',
        duration=duration,
        execution='hold')
