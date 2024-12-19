from garminworkouts.config.generators.strength.other import (
    plank_shoulder_tap_rep_generator,
    climber_rep_generator,
    leg_raise_rep_generator,
    leg_raise_hold_generator,
    max_pushup_generator,
    reverse_angel_rep_generator,
    up_down_plank_generator,
    elbow_plank_hold_generator,
    circle_generator,
    high_crunch,
    plank_rotation_generator,
    plank_walkout_generator,
    plank_armleglift_generator,
    leg_circle_generator,
    high_crunch_generator,
    rest_generator,
    mountain_climber_rep_generator,
    lying_straight_leg_raise_rep_generator,
    lying_straight_leg_raise_hold_generator,
    lying_external_rotation_rep_generator,
    elbow_plank_pike_jacks_rep_generator,
    elbow_plank_pike_jacks_hold_generator,
    flutter_kicks_hold_generator,
    crunch_rep_generator,
    plank_with_leg_lift_rep_generator
)


def test_plank_shoulder_tap_rep_generator():
    duration = 30
    result = plank_shoulder_tap_rep_generator(duration)
    assert result == {
        'type': 'interval',
        'duration': f'{duration}reps',
        'target': 'NO_TARGET',
        'description': 'Straight Arm Plank With Shoulder Touch',
        'category': 'PLANK',
        'exerciseName': 'STRAIGHT_ARM_PLANK_WITH_SHOULDER_TOUCH',
    }


def test_climber_rep_generator():
    duration = 30
    result = climber_rep_generator(duration)
    assert result == mountain_climber_rep_generator(duration)


def test_leg_raise_rep_generator():
    duration = 30
    result = leg_raise_rep_generator(duration)
    assert result == lying_straight_leg_raise_rep_generator(duration)


def test_leg_raise_hold_generator():
    duration = 30
    result = leg_raise_hold_generator(duration)
    assert result == lying_straight_leg_raise_hold_generator(duration)


def test_max_pushup_generator():
    result = max_pushup_generator()
    assert result == {
        'type': 'interval',
        'duration': 'lap.button',
        'target': 'NO_TARGET',
        'description': 'Max Push Ups',
        'category': 'PUSH_UP',
        'exerciseName': 'PUSH_UP',
    }


def test_reverse_angel_rep_generator():
    duration = 30
    result = reverse_angel_rep_generator(duration)
    assert result == lying_external_rotation_rep_generator(duration)


def test_up_down_plank_generator():
    duration = 30
    result = up_down_plank_generator(duration)
    assert result == elbow_plank_pike_jacks_rep_generator(duration)


def test_elbow_plank_hold_generator():
    duration = 30
    result = elbow_plank_hold_generator(duration)
    assert result == elbow_plank_pike_jacks_hold_generator(duration)


def test_circle_generator():
    duration = 30
    result = circle_generator(duration)
    assert result == flutter_kicks_hold_generator(duration)


def test_high_crunch():
    duration = 30
    result = high_crunch(duration)
    assert result == crunch_rep_generator(duration)


def test_plank_rotation_generator():
    duration = 30
    result = plank_rotation_generator(duration)
    assert result == {
        'type': 'interval',
        'duration': f'{duration}reps',
        'target': 'NO_TARGET',
        'description': 'Plank With Arm Raise',
        'category': 'PLANK',
        'exerciseName': 'PLANK_WITH_ARM_RAISE',
    }


def test_plank_walkout_generator():
    duration = 30
    result = plank_walkout_generator(duration)
    assert result == {
        'type': 'interval',
        'duration': f'{duration}reps',
        'target': 'NO_TARGET',
        'description': 'Plank To Stand Up',
        'category': 'PLANK',
        'exerciseName': 'PLANK_TO_STAND_UP',
    }


def test_plank_armleglift_generator():
    duration = 30
    result = plank_armleglift_generator(duration)
    assert result == plank_with_leg_lift_rep_generator(duration)


def test_leg_circle_generator():
    duration = 30
    result = leg_circle_generator(duration)
    assert result == flutter_kicks_hold_generator(duration)


def test_high_crunch_generator():
    duration = 30
    result = high_crunch_generator(duration)
    assert result == crunch_rep_generator(duration)


def test_rest_generator():
    duration = 30
    result = rest_generator(duration)
    assert result == {
        'type': 'rest',
        'duration': duration,
        'target': 'NO_TARGET',
        'description': '',
        'category': None,
        'exerciseName': None
    }
