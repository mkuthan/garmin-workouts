import pytest

from garminworkouts.config.generators.strength.multi_step import (
    plank_push_hold_generator, calf_lunge_side_generator, calf_lunge_squat_generator,
    calf_hold_lunge_generator, calf_hold_squat_generator, calf_squat_hold_generator,
    plank_push_angel_generator, climber_shoulder_tap_plank_rot_generator,
    leg_raise_hold_situp_generator, leg_raise_hold_kneetwist_generator,
    max_pushups_generator, shoulder_tap_updown_plank_hold_generator,
    shoulder_tap_plank_rotation_updown_plank_generator, flutter_kick_circle_high_crunch_generator,
    flutter_kick_heeltap_crunch_generator, plank_rotation_walkout_altraises_generator
)


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_plank_push_hold_generator(duration):
    steps = plank_push_hold_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == f'{int(int(duration)/2)}reps'
    assert steps[2]['duration'] == 'lap.button'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_calf_lunge_side_generator(duration):
    steps = calf_lunge_side_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == f'{duration}reps'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_calf_lunge_squat_generator(duration):
    steps = calf_lunge_squat_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == f'{duration}reps'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_calf_hold_lunge_generator(duration):
    steps = calf_hold_lunge_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == 'lap.button'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_calf_hold_squat_generator(duration):
    steps = calf_hold_squat_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == 'lap.button'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_calf_squat_hold_generator(duration):
    steps = calf_squat_hold_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == f'{duration}reps'
    assert steps[2]['duration'] == 'lap.button'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_plank_push_angel_generator(duration):
    steps = plank_push_angel_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == f'{int(int(duration)/2)}reps'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_climber_shoulder_tap_plank_rot_generator(duration):
    steps = climber_shoulder_tap_plank_rot_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == f'{duration}reps'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_leg_raise_hold_situp_generator(duration):
    steps = leg_raise_hold_situp_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == 'lap.button'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_leg_raise_hold_kneetwist_generator(duration):
    steps = leg_raise_hold_kneetwist_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == 'lap.button'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_max_pushups_generator(duration):
    steps = max_pushups_generator(duration)
    assert len(steps) == 2
    assert steps[0]['duration'] == 'lap.button'
    assert steps[1]['type'] == 'rest'
    assert steps[1]['duration'] == '0:30'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_shoulder_tap_updown_plank_hold_generator(duration):
    steps = shoulder_tap_updown_plank_hold_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == f'{int(int(duration)/2)}reps'
    assert steps[2]['duration'] == 'lap.button'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_shoulder_tap_plank_rotation_updown_plank_generator(duration):
    steps = shoulder_tap_plank_rotation_updown_plank_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == f'{duration}reps'
    assert steps[2]['duration'] == f'{int(int(duration)/2)}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_flutter_kick_circle_high_crunch_generator(duration):
    steps = flutter_kick_circle_high_crunch_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == 'lap.button'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_flutter_kick_heeltap_crunch_generator(duration):
    steps = flutter_kick_heeltap_crunch_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == 'lap.button'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'


@pytest.mark.parametrize("duration", ["10", "20", "30"])
def test_plank_rotation_walkout_altraises_generator(duration):
    steps = plank_rotation_walkout_altraises_generator(duration)
    assert len(steps) == 4
    assert steps[0]['duration'] == f'{duration}reps'
    assert steps[1]['duration'] == f'{int(int(duration)/2)}reps'
    assert steps[2]['duration'] == f'{duration}reps'
    assert steps[3]['type'] == 'rest'
    assert steps[3]['duration'] == '2:00'
