from garminworkouts.config.generators.base import step_generator
from garminworkouts.models.strength_map import MAP


def plank_shoulder_tap_rep_generator(duration) -> dict:
    return exercise_generator(
        category='PLANK',
        exercise_name='STRAIGHT_ARM_PLANK_WITH_SHOULDER_TOUCH',
        duration=duration,
        execution='reps')


def side_plank_rep_generator(duration) -> dict:
    return exercise_generator(
        category='PLANK',
        exercise_name='SIDE_PLANK',
        duration=duration,
        execution='reps')


def climber_rep_generator(duration) -> dict:
    return exercise_generator(
        category='PLANK',
        exercise_name='MOUNTAIN_CLIMBER',
        duration=duration,
        execution='reps')


def plank_hold_generator(duration) -> dict:
    return exercise_generator(
        category='PLANK',
        exercise_name='PLANK',
        duration=duration,
        execution='hold')


def calf_raise_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CALF_RAISE',
        exercise_name='CALF_RAISE',
        duration=duration,
        execution='reps')


def calf_raise_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CALF_RAISE',
        exercise_name='CALF_RAISE',
        duration=duration,
        execution='hold')


def leg_raise_rep_generator(duration) -> dict:
    return exercise_generator(
        category='LEG_RAISE',
        exercise_name='HANGING_LEG_RAISE',
        duration=duration,
        execution='reps')


def leg_raise_hold_generator(duration) -> dict:
    return exercise_generator(
        category='LEG_RAISE',
        exercise_name='HANGING_LEG_RAISE',
        duration=duration,
        execution='hold')


def lunge_rep_generator(duration) -> dict:
    return exercise_generator(
        category='LUNGE',
        exercise_name='LUNGE',
        duration=duration,
        execution='reps')


def side_lunge_rep_generator(duration) -> dict:
    return exercise_generator(
        category='LUNGE',
        exercise_name='SIDE_LUNGE',
        duration=duration,
        execution='reps')


def pushup_rep_generator(duration) -> dict:
    return exercise_generator(
        category='PUSH_UP',
        exercise_name='PUSH_UP',
        duration=duration,
        execution='reps')


def max_pushup_generator() -> dict:
    return exercise_generator(
        category='PUSH_UP',
        exercise_name='PUSH_UP',
        execution='max')


def situp_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SIT_UP',
        exercise_name='SIT_UP',
        duration=duration,
        execution='reps')


def squat_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SQUAT',
        exercise_name='SQUAT',
        duration=duration,
        execution='reps')


def squat_hold_generator(duration) -> dict:
    return exercise_generator(
        category='SQUAT',
        exercise_name='SQUAT',
        duration=duration,
        execution='hold')


def reverse_angel_rep_generator(duration) -> dict:
    return exercise_generator(
        category='SHOULDER_STABILITY',
        exercise_name='LYING_EXTERNAL_ROTATION',
        duration=duration,
        execution='reps')


def exercise_generator(category='', exercise_name='', duration='', execution='') -> dict:
    if category not in MAP:
        raise KeyError(f"Category {category} not found in strength exercises.")
    else:
        fields = MAP[category]

    if exercise_name not in fields:
        raise ValueError(f"Exercise {exercise_name} not found in {category}.")

    description: str = exercise_name.replace('_', ' ').title()

    if execution == 'reps':
        return step_generator(
            category=category,
            description=description,
            duration=f"{duration}reps",
            exerciseName=exercise_name)
    elif execution == 'hold':
        return step_generator(
            category=category,
            description=f"{duration}-count hold",
            duration='lap.button',
            exerciseName=exercise_name)
    else:
        return step_generator(
            category=category,
            description=f"Max {description}s",
            duration='lap.button',
            exerciseName=exercise_name)


def rest_generator(duration) -> dict:
    return step_generator(
        type='rest',
        duration=duration)
