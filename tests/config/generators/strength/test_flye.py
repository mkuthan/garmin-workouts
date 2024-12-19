import pytest

from garminworkouts.config.generators.strength.flye import (
    cable_crossover_rep_generator,
    cable_crossover_hold_generator,
    decline_dumbbell_flye_rep_generator,
    decline_dumbbell_flye_hold_generator,
    dumbbell_flye_rep_generator,
    dumbbell_flye_hold_generator,
    incline_dumbbell_flye_rep_generator,
    incline_dumbbell_flye_hold_generator,
    incline_reverse_flye_rep_generator,
    incline_reverse_flye_hold_generator,
    kettlebell_flye_rep_generator,
    kettlebell_flye_hold_generator,
    kneeling_rear_flye_rep_generator,
    kneeling_rear_flye_hold_generator,
    single_arm_standing_cable_reverse_flye_rep_generator,
    single_arm_standing_cable_reverse_flye_hold_generator,
    swiss_ball_dumbbell_flye_rep_generator,
    swiss_ball_dumbbell_flye_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (cable_crossover_rep_generator, 'CABLE_CROSSOVER', 'reps'),
    (cable_crossover_hold_generator, 'CABLE_CROSSOVER', 'hold'),
    (decline_dumbbell_flye_rep_generator, 'DECLINE_DUMBBELL_FLYE', 'reps'),
    (decline_dumbbell_flye_hold_generator, 'DECLINE_DUMBBELL_FLYE', 'hold'),
    (dumbbell_flye_rep_generator, 'DUMBBELL_FLYE', 'reps'),
    (dumbbell_flye_hold_generator, 'DUMBBELL_FLYE', 'hold'),
    (incline_dumbbell_flye_rep_generator, 'INCLINE_DUMBBELL_FLYE', 'reps'),
    (incline_dumbbell_flye_hold_generator, 'INCLINE_DUMBBELL_FLYE', 'hold'),
    (incline_reverse_flye_rep_generator, 'INCLINE_REVERSE_FLYE', 'reps'),
    (incline_reverse_flye_hold_generator, 'INCLINE_REVERSE_FLYE', 'hold'),
    (kettlebell_flye_rep_generator, 'KETTLEBELL_FLYE', 'reps'),
    (kettlebell_flye_hold_generator, 'KETTLEBELL_FLYE', 'hold'),
    (kneeling_rear_flye_rep_generator, 'KNEELING_REAR_FLYE', 'reps'),
    (kneeling_rear_flye_hold_generator, 'KNEELING_REAR_FLYE', 'hold'),
    (single_arm_standing_cable_reverse_flye_rep_generator, 'SINGLE_ARM_STANDING_CABLE_REVERSE_FLYE', 'reps'),
    (single_arm_standing_cable_reverse_flye_hold_generator, 'SINGLE_ARM_STANDING_CABLE_REVERSE_FLYE', 'hold'),
    (swiss_ball_dumbbell_flye_rep_generator, 'SWISS_BALL_DUMBBELL_FLYE', 'reps'),
    (swiss_ball_dumbbell_flye_hold_generator, 'SWISS_BALL_DUMBBELL_FLYE', 'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'FLYE'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
