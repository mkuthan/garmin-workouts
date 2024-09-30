from garminworkouts.config.generators.base import step_generator
from garminworkouts.config.generators.strength.crunch import crunch_rep_generator, flutter_kicks_hold_generator
from garminworkouts.config.generators.strength.leg_raise import (lying_straight_leg_raise_hold_generator,
                                                                 lying_straight_leg_raise_rep_generator)
from garminworkouts.config.generators.strength.plank import (elbow_plank_pike_jacks_hold_generator,
                                                             elbow_plank_pike_jacks_rep_generator,
                                                             mountain_climber_rep_generator,
                                                             plank_with_leg_lift_rep_generator)
from garminworkouts.config.generators.strength.shoulder_stability import lying_external_rotation_rep_generator
from garminworkouts.config.generators.strength.simple_step import exercise_generator


def plank_shoulder_tap_rep_generator(duration) -> dict:
    return exercise_generator(
        category='PLANK',
        exercise_name='STRAIGHT_ARM_PLANK_WITH_SHOULDER_TOUCH',
        duration=duration,
        execution='reps')


def climber_rep_generator(duration) -> dict:
    return mountain_climber_rep_generator(duration)


def leg_raise_rep_generator(duration) -> dict:
    return lying_straight_leg_raise_rep_generator(duration)


def leg_raise_hold_generator(duration) -> dict:
    return lying_straight_leg_raise_hold_generator(duration)


def max_pushup_generator() -> dict:
    return exercise_generator(
        category='PUSH_UP',
        exercise_name='PUSH_UP',
        execution='max')


def reverse_angel_rep_generator(duration) -> dict:
    return lying_external_rotation_rep_generator(duration)


def up_down_plank_generator(duration) -> dict:
    return elbow_plank_pike_jacks_rep_generator(duration)


def elbow_plank_hold_generator(duration) -> dict:
    return elbow_plank_pike_jacks_hold_generator(duration)


def circle_generator(duration) -> dict:
    return flutter_kicks_hold_generator(duration)


def high_crunch(duration) -> dict:
    return crunch_rep_generator(duration)


def plank_rotation_generator(duration) -> dict:
    return exercise_generator(
        category='PLANK',
        exercise_name='PLANK_WITH_ARM_RAISE',
        duration=duration,
        execution='reps')


def plank_walkout_generator(duration) -> dict:
    return exercise_generator(
        category='PLANK',
        exercise_name='PLANK_TO_STAND_UP',
        duration=duration,
        execution='reps')


def plank_armleglift_generator(duration) -> dict:
    return plank_with_leg_lift_rep_generator(duration)


def leg_circle_generator(duration) -> dict:
    return flutter_kicks_hold_generator(duration)


def high_crunch_generator(duration) -> dict:
    return crunch_rep_generator(duration)


def rest_generator(duration) -> dict:
    return step_generator(
        type='rest',
        duration=duration)
