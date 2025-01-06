from garminworkouts.config.generators.strength.banded_exercises import (lunge_rep_generator, plank_hold_generator,
                                                                        squat_hold_generator, squat_rep_generator)
from garminworkouts.config.generators.strength.calf_raise import calf_raise_hold_generator, calf_raise_rep_generator
from garminworkouts.config.generators.strength.crunch import flutter_kicks_rep_generator
from garminworkouts.config.generators.strength.lunge import side_lunge_rep_generator
from garminworkouts.config.generators.strength.plank import plank_knee_twist_rep_generator, side_plank_rep_generator
from garminworkouts.config.generators.strength.push_up import push_up_rep_generator
from garminworkouts.config.generators.strength.other import (climber_rep_generator, high_crunch_generator,
                                                             leg_circle_generator, leg_raise_hold_generator,
                                                             leg_raise_rep_generator,
                                                             max_pushup_generator,
                                                             plank_armleglift_generator,
                                                             plank_rotation_generator,
                                                             plank_shoulder_tap_rep_generator,
                                                             plank_walkout_generator,
                                                             rest_generator, reverse_angel_rep_generator,
                                                             up_down_plank_generator)
from garminworkouts.config.generators.strength.sit_up import sit_up_rep_generator


def plank_push_hold_generator(duration) -> list[dict]:
    steps: list[dict] = []
    med = str(int(int(duration) / 2))
    steps.append(plank_shoulder_tap_rep_generator(duration))
    steps.append(push_up_rep_generator(med))
    steps.append(plank_hold_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def calf_lunge_side_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(calf_raise_rep_generator(duration))
    steps.append(lunge_rep_generator(duration))
    steps.append(side_lunge_rep_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def calf_lunge_squat_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(calf_raise_rep_generator(duration))
    steps.append(lunge_rep_generator(duration))
    steps.append(squat_rep_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def calf_hold_lunge_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(calf_raise_rep_generator(duration))
    steps.append(calf_raise_hold_generator(duration))
    steps.append(lunge_rep_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def calf_hold_squat_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(calf_raise_rep_generator(duration))
    steps.append(calf_raise_hold_generator(duration))
    steps.append(squat_rep_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def calf_squat_hold_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(calf_raise_rep_generator(duration))
    steps.append(squat_rep_generator(duration))
    steps.append(squat_hold_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def plank_push_angel_generator(duration) -> list[dict]:
    steps: list[dict] = []
    med = str(int(int(duration) / 2))
    steps.append(plank_shoulder_tap_rep_generator(duration))
    steps.append(push_up_rep_generator(med))
    steps.append(reverse_angel_rep_generator(duration))
    steps.append(rest_generator('2:00'))

    return steps


def climber_shoulder_tap_plank_rot_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(climber_rep_generator(duration))
    steps.append(plank_shoulder_tap_rep_generator(duration))
    steps.append(side_plank_rep_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def leg_raise_hold_situp_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(leg_raise_rep_generator(duration))
    steps.append(leg_raise_hold_generator(duration))
    steps.append(sit_up_rep_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def leg_raise_hold_kneetwist_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(leg_raise_rep_generator(duration))
    steps.append(leg_raise_hold_generator(duration))
    steps.append(plank_knee_twist_rep_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def max_pushups_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(max_pushup_generator())
    steps.append(rest_generator('0:30'))
    return steps


def shoulder_tap_updown_plank_hold_generator(duration) -> list[dict]:
    steps: list[dict] = []
    med = str(int(int(duration) / 2))
    steps.append(plank_shoulder_tap_rep_generator(duration))
    steps.append(up_down_plank_generator(med))
    steps.append(plank_hold_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def shoulder_tap_plank_rotation_updown_plank_generator(duration) -> list[dict]:
    steps: list[dict] = []
    med = str(int(int(duration) / 2))
    steps.append(plank_shoulder_tap_rep_generator(duration))
    steps.append(plank_rotation_generator(duration))
    steps.append(up_down_plank_generator(med))
    steps.append(rest_generator('2:00'))
    return steps


def flutter_kick_circle_high_crunch_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(flutter_kicks_rep_generator(duration))
    steps.append(leg_circle_generator(duration))
    steps.append(high_crunch_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def flutter_kick_heeltap_crunch_generator(duration) -> list[dict]:
    steps: list[dict] = []
    steps.append(flutter_kicks_rep_generator(duration))
    steps.append(leg_circle_generator(duration))
    steps.append(high_crunch_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps


def plank_rotation_walkout_altraises_generator(duration) -> list[dict]:
    steps: list[dict] = []
    med = str(int(int(duration) / 2))
    steps.append(plank_rotation_generator(duration))
    steps.append(plank_walkout_generator(med))
    steps.append(plank_armleglift_generator(duration))
    steps.append(rest_generator('2:00'))
    return steps
