from garminworkouts.config.generators.strength.simple_step import exercise_generator


def bar_holds_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='BAR_HOLDS',
        duration=duration,
        execution='reps')


def bar_holds_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='BAR_HOLDS',
        duration=duration,
        execution='hold')


def carry_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='CARRY',
        duration=duration,
        execution='reps')


def carry_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='CARRY',
        duration=duration,
        execution='hold')


def dumbbell_waiter_carry_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='DUMBBELL_WAITER_CARRY',
        duration=duration,
        execution='reps')


def dumbbell_waiter_carry_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='DUMBBELL_WAITER_CARRY',
        duration=duration,
        execution='hold')


def farmers_carry_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='FARMERS_CARRY',
        duration=duration,
        execution='reps')


def farmers_carry_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='FARMERS_CARRY',
        duration=duration,
        execution='hold')


def farmers_carry_on_toes_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='FARMERS_CARRY_ON_TOES',
        duration=duration,
        execution='reps')


def farmers_carry_on_toes_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='FARMERS_CARRY_ON_TOES',
        duration=duration,
        execution='hold')


def farmers_carry_walk_lunge_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='FARMERS_CARRY_WALK_LUNGE',
        duration=duration,
        execution='reps')


def farmers_carry_walk_lunge_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='FARMERS_CARRY_WALK_LUNGE',
        duration=duration,
        execution='hold')


def farmers_walk_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='FARMERS_WALK',
        duration=duration,
        execution='reps')


def farmers_walk_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='FARMERS_WALK',
        duration=duration,
        execution='hold')


def farmers_walk_on_toes_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='FARMERS_WALK_ON_TOES',
        duration=duration,
        execution='reps')


def farmers_walk_on_toes_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='FARMERS_WALK_ON_TOES',
        duration=duration,
        execution='hold')


def hex_dumbbell_hold_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='HEX_DUMBBELL_HOLD',
        duration=duration,
        execution='reps')


def hex_dumbbell_hold_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='HEX_DUMBBELL_HOLD',
        duration=duration,
        execution='hold')


def overhead_carry_rep_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='OVERHEAD_CARRY',
        duration=duration,
        execution='reps')


def overhead_carry_hold_generator(duration) -> dict:
    return exercise_generator(
        category='CARRY',
        exercise_name='OVERHEAD_CARRY',
        duration=duration,
        execution='hold')
