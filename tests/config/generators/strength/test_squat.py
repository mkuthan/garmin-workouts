import pytest

from garminworkouts.config.generators.strength.squat import (
    air_squat_rep_generator,
    air_squat_hold_generator,
    alternating_box_dumbbell_step_ups_rep_generator,
    alternating_box_dumbbell_step_ups_hold_generator,
    back_squat_with_body_bar_rep_generator,
    back_squat_with_body_bar_hold_generator,
    back_squats_rep_generator,
    back_squats_hold_generator,
    balancing_squat_rep_generator,
    balancing_squat_hold_generator,
    barbell_back_squat_rep_generator,
    barbell_back_squat_hold_generator,
    barbell_box_squat_rep_generator,
    barbell_box_squat_hold_generator,
    barbell_front_squat_rep_generator,
    barbell_front_squat_hold_generator,
    barbell_hack_squat_rep_generator,
    barbell_hack_squat_hold_generator,
    barbell_hang_squat_snatch_rep_generator,
    barbell_hang_squat_snatch_hold_generator,
    barbell_lateral_step_up_rep_generator,
    barbell_lateral_step_up_hold_generator,
    barbell_quarter_squat_rep_generator,
    barbell_quarter_squat_hold_generator,
    barbell_siff_squat_rep_generator,
    barbell_siff_squat_hold_generator,
    barbell_squat_snatch_rep_generator,
    barbell_squat_snatch_hold_generator,
    barbell_squat_with_heels_raised_rep_generator,
    barbell_squat_with_heels_raised_hold_generator,
    barbell_step_up_rep_generator,
    barbell_step_up_hold_generator,
    barbell_stepover_rep_generator,
    barbell_stepover_hold_generator,
    bench_squat_with_rotational_chop_rep_generator,
    bench_squat_with_rotational_chop_hold_generator,
    body_weight_wall_squat_rep_generator,
    body_weight_wall_squat_hold_generator,
    box_step_squat_rep_generator,
    box_step_squat_hold_generator,
    braced_squat_rep_generator,
    braced_squat_hold_generator,
    crossed_arm_barbell_front_squat_rep_generator,
    crossed_arm_barbell_front_squat_hold_generator,
    crossover_dumbbell_step_up_rep_generator,
    crossover_dumbbell_step_up_hold_generator,
    dumbbell_front_squat_rep_generator,
    dumbbell_front_squat_hold_generator,
    dumbbell_overhead_squat_single_arm_rep_generator,
    dumbbell_overhead_squat_single_arm_hold_generator,
    dumbbell_split_squat_rep_generator,
    dumbbell_split_squat_hold_generator,
    dumbbell_squat_rep_generator,
    dumbbell_squat_hold_generator,
    dumbbell_squat_clean_rep_generator,
    dumbbell_squat_clean_hold_generator,
    dumbbell_squat_snatch_rep_generator,
    dumbbell_squat_snatch_hold_generator,
    dumbbell_step_up_rep_generator,
    dumbbell_step_up_hold_generator,
    dumbbell_stepover_rep_generator,
    dumbbell_stepover_hold_generator,
    dumbbell_thrusters_rep_generator,
    dumbbell_thrusters_hold_generator,
    elevated_single_leg_squat_rep_generator,
    elevated_single_leg_squat_hold_generator,
    figure_four_squats_rep_generator,
    figure_four_squats_hold_generator,
    goblet_squat_rep_generator,
    goblet_squat_hold_generator,
    kettlebell_squat_rep_generator,
    kettlebell_squat_hold_generator,
    kettlebell_swing_overhead_rep_generator,
    kettlebell_swing_overhead_hold_generator,
    kettlebell_swing_with_flip_to_squat_rep_generator,
    kettlebell_swing_with_flip_to_squat_hold_generator,
    lateral_dumbbell_step_up_rep_generator,
    lateral_dumbbell_step_up_hold_generator,
    leg_press_rep_generator,
    leg_press_hold_generator,
    medicine_ball_squat_rep_generator,
    medicine_ball_squat_hold_generator,
    one_legged_squat_rep_generator,
    one_legged_squat_hold_generator,
    overhead_barbell_squat_rep_generator,
    overhead_barbell_squat_hold_generator,
    overhead_dumbbell_squat_rep_generator,
    overhead_dumbbell_squat_hold_generator,
    overhead_squat_rep_generator,
    overhead_squat_hold_generator,
    partial_single_leg_squat_rep_generator,
    partial_single_leg_squat_hold_generator,
    pistol_squat_rep_generator,
    pistol_squat_hold_generator,
    plie_slides_rep_generator,
    plie_slides_hold_generator,
    plie_squat_rep_generator,
    plie_squat_hold_generator,
    prisoner_squat_rep_generator,
    prisoner_squat_hold_generator,
    single_leg_bench_get_up_rep_generator,
    single_leg_bench_get_up_hold_generator,
    single_leg_bench_squat_rep_generator,
    single_leg_bench_squat_hold_generator,
    single_leg_squat_on_swiss_ball_rep_generator,
    single_leg_squat_on_swiss_ball_hold_generator,
    squat_rep_generator,
    squat_hold_generator,
    squat_american_swing_rep_generator,
    squat_american_swing_hold_generator,
    squat_and_side_kick_rep_generator,
    squat_and_side_kick_hold_generator,
    squat_jumps_in_n_out_rep_generator,
    squat_jumps_in_n_out_hold_generator,
    squats_with_band_rep_generator,
    squats_with_band_hold_generator,
    staggered_squat_rep_generator,
    staggered_squat_hold_generator,
    step_up_rep_generator,
    step_up_hold_generator,
    suitcase_squats_rep_generator,
    suitcase_squats_hold_generator,
    sumo_squat_rep_generator,
    sumo_squat_hold_generator,
    sumo_squat_slide_in_rep_generator,
    sumo_squat_slide_in_hold_generator,
    sumo_squat_to_high_pull_rep_generator,
    sumo_squat_to_high_pull_hold_generator,
    sumo_squat_to_stand_rep_generator,
    sumo_squat_to_stand_hold_generator,
    sumo_squat_with_rotation_rep_generator,
    sumo_squat_with_rotation_hold_generator,
    swiss_ball_body_weight_wall_squat_rep_generator,
    swiss_ball_body_weight_wall_squat_hold_generator,
    thrusters_rep_generator,
    thrusters_hold_generator,
    uneven_squat_rep_generator,
    uneven_squat_hold_generator,
    waist_slimming_squat_rep_generator,
    waist_slimming_squat_hold_generator,
    wall_ball_rep_generator,
    wall_ball_hold_generator,
    wall_ball_squat_and_press_rep_generator,
    wall_ball_squat_and_press_hold_generator,
    weighted_back_squats_rep_generator,
    weighted_back_squats_hold_generator,
    weighted_balancing_squat_rep_generator,
    weighted_balancing_squat_hold_generator,
    weighted_bench_squat_with_rotational_chop_rep_generator,
    weighted_bench_squat_with_rotational_chop_hold_generator,
    weighted_box_step_squat_rep_generator,
    weighted_box_step_squat_hold_generator,
    weighted_elevated_single_leg_squat_rep_generator,
    weighted_elevated_single_leg_squat_hold_generator,
    weighted_figure_four_squats_rep_generator,
    weighted_figure_four_squats_hold_generator,
    weighted_partial_single_leg_squat_rep_generator,
    weighted_partial_single_leg_squat_hold_generator,
    weighted_pistol_squat_rep_generator,
    weighted_pistol_squat_hold_generator,
    weighted_plie_slides_rep_generator,
    weighted_plie_slides_hold_generator,
    weighted_plie_squat_rep_generator,
    weighted_plie_squat_hold_generator,
    weighted_prisoner_squat_rep_generator,
    weighted_prisoner_squat_hold_generator,
    weighted_single_leg_bench_get_up_rep_generator,
    weighted_single_leg_bench_get_up_hold_generator,
    weighted_single_leg_bench_squat_rep_generator,
    weighted_single_leg_bench_squat_hold_generator,
    weighted_single_leg_squat_on_swiss_ball_rep_generator,
    weighted_single_leg_squat_on_swiss_ball_hold_generator,
    weighted_squat_rep_generator,
    weighted_squat_hold_generator,
    weighted_staggered_squat_rep_generator,
    weighted_staggered_squat_hold_generator,
    weighted_step_up_rep_generator,
    weighted_step_up_hold_generator,
    weighted_sumo_squat_slide_in_rep_generator,
    weighted_sumo_squat_slide_in_hold_generator,
    weighted_sumo_squat_to_stand_rep_generator,
    weighted_sumo_squat_to_stand_hold_generator,
    weighted_sumo_squat_with_rotation_rep_generator,
    weighted_sumo_squat_with_rotation_hold_generator,
    weighted_swiss_ball_wall_squat_rep_generator,
    weighted_swiss_ball_wall_squat_hold_generator,
    weighted_uneven_squat_rep_generator,
    weighted_uneven_squat_hold_generator,
    weighted_wall_squat_rep_generator,
    weighted_wall_squat_hold_generator,
    wide_stance_barbell_squat_rep_generator,
    wide_stance_barbell_squat_hold_generator,
    wide_stance_goblet_squat_rep_generator,
    wide_stance_goblet_squat_hold_generator,
    zercher_squat_rep_generator,
    zercher_squat_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (air_squat_rep_generator, 'AIR_SQUAT', 'reps'),
    (air_squat_hold_generator, 'AIR_SQUAT', 'hold'),
    (alternating_box_dumbbell_step_ups_rep_generator, 'ALTERNATING_BOX_DUMBBELL_STEP_UPS', 'reps'),
    (alternating_box_dumbbell_step_ups_hold_generator, 'ALTERNATING_BOX_DUMBBELL_STEP_UPS', 'hold'),
    (back_squat_with_body_bar_rep_generator, 'BACK_SQUAT_WITH_BODY_BAR', 'reps'),
    (back_squat_with_body_bar_hold_generator, 'BACK_SQUAT_WITH_BODY_BAR', 'hold'),
    (back_squats_rep_generator, 'BACK_SQUATS', 'reps'),
    (back_squats_hold_generator, 'BACK_SQUATS', 'hold'),
    (balancing_squat_rep_generator, 'BALANCING_SQUAT', 'reps'),
    (balancing_squat_hold_generator, 'BALANCING_SQUAT', 'hold'),
    (barbell_back_squat_rep_generator, 'BARBELL_BACK_SQUAT', 'reps'),
    (barbell_back_squat_hold_generator, 'BARBELL_BACK_SQUAT', 'hold'),
    (barbell_box_squat_rep_generator, 'BARBELL_BOX_SQUAT', 'reps'),
    (barbell_box_squat_hold_generator, 'BARBELL_BOX_SQUAT', 'hold'),
    (barbell_front_squat_rep_generator, 'BARBELL_FRONT_SQUAT', 'reps'),
    (barbell_front_squat_hold_generator, 'BARBELL_FRONT_SQUAT', 'hold'),
    (barbell_hack_squat_rep_generator, 'BARBELL_HACK_SQUAT', 'reps'),
    (barbell_hack_squat_hold_generator, 'BARBELL_HACK_SQUAT', 'hold'),
    (barbell_hang_squat_snatch_rep_generator, 'BARBELL_HANG_SQUAT_SNATCH', 'reps'),
    (barbell_hang_squat_snatch_hold_generator, 'BARBELL_HANG_SQUAT_SNATCH', 'hold'),
    (barbell_lateral_step_up_rep_generator, 'BARBELL_LATERAL_STEP_UP', 'reps'),
    (barbell_lateral_step_up_hold_generator, 'BARBELL_LATERAL_STEP_UP', 'hold'),
    (barbell_quarter_squat_rep_generator, 'BARBELL_QUARTER_SQUAT', 'reps'),
    (barbell_quarter_squat_hold_generator, 'BARBELL_QUARTER_SQUAT', 'hold'),
    (barbell_siff_squat_rep_generator, 'BARBELL_SIFF_SQUAT', 'reps'),
    (barbell_siff_squat_hold_generator, 'BARBELL_SIFF_SQUAT', 'hold'),
    (barbell_squat_snatch_rep_generator, 'BARBELL_SQUAT_SNATCH', 'reps'),
    (barbell_squat_snatch_hold_generator, 'BARBELL_SQUAT_SNATCH', 'hold'),
    (barbell_squat_with_heels_raised_rep_generator, 'BARBELL_SQUAT_WITH_HEELS_RAISED', 'reps'),
    (barbell_squat_with_heels_raised_hold_generator, 'BARBELL_SQUAT_WITH_HEELS_RAISED', 'hold'),
    (barbell_step_up_rep_generator, 'BARBELL_STEP_UP', 'reps'),
    (barbell_step_up_hold_generator, 'BARBELL_STEP_UP', 'hold'),
    (barbell_stepover_rep_generator, 'BARBELL_STEPOVER', 'reps'),
    (barbell_stepover_hold_generator, 'BARBELL_STEPOVER', 'hold'),
    (bench_squat_with_rotational_chop_rep_generator, 'BENCH_SQUAT_WITH_ROTATIONAL_CHOP', 'reps'),
    (bench_squat_with_rotational_chop_hold_generator, 'BENCH_SQUAT_WITH_ROTATIONAL_CHOP', 'hold'),
    (body_weight_wall_squat_rep_generator, 'BODY_WEIGHT_WALL_SQUAT', 'reps'),
    (body_weight_wall_squat_hold_generator, 'BODY_WEIGHT_WALL_SQUAT', 'hold'),
    (box_step_squat_rep_generator, 'BOX_STEP_SQUAT', 'reps'),
    (box_step_squat_hold_generator, 'BOX_STEP_SQUAT', 'hold'),
    (braced_squat_rep_generator, 'BRACED_SQUAT', 'reps'),
    (braced_squat_hold_generator, 'BRACED_SQUAT', 'hold'),
    (crossed_arm_barbell_front_squat_rep_generator, 'CROSSED_ARM_BARBELL_FRONT_SQUAT', 'reps'),
    (crossed_arm_barbell_front_squat_hold_generator, 'CROSSED_ARM_BARBELL_FRONT_SQUAT', 'hold'),
    (crossover_dumbbell_step_up_rep_generator, 'CROSSOVER_DUMBBELL_STEP_UP', 'reps'),
    (crossover_dumbbell_step_up_hold_generator, 'CROSSOVER_DUMBBELL_STEP_UP', 'hold'),
    (dumbbell_front_squat_rep_generator, 'DUMBBELL_FRONT_SQUAT', 'reps'),
    (dumbbell_front_squat_hold_generator, 'DUMBBELL_FRONT_SQUAT', 'hold'),
    (dumbbell_overhead_squat_single_arm_rep_generator, 'DUMBBELL_OVERHEAD_SQUAT_SINGLE_ARM', 'reps'),
    (dumbbell_overhead_squat_single_arm_hold_generator, 'DUMBBELL_OVERHEAD_SQUAT_SINGLE_ARM', 'hold'),
    (dumbbell_split_squat_rep_generator, 'DUMBBELL_SPLIT_SQUAT', 'reps'),
    (dumbbell_split_squat_hold_generator, 'DUMBBELL_SPLIT_SQUAT', 'hold'),
    (dumbbell_squat_rep_generator, 'DUMBBELL_SQUAT', 'reps'),
    (dumbbell_squat_hold_generator, 'DUMBBELL_SQUAT', 'hold'),
    (dumbbell_squat_clean_rep_generator, 'DUMBBELL_SQUAT_CLEAN', 'reps'),
    (dumbbell_squat_clean_hold_generator, 'DUMBBELL_SQUAT_CLEAN', 'hold'),
    (dumbbell_squat_snatch_rep_generator, 'DUMBBELL_SQUAT_SNATCH', 'reps'),
    (dumbbell_squat_snatch_hold_generator, 'DUMBBELL_SQUAT_SNATCH', 'hold'),
    (dumbbell_step_up_rep_generator, 'DUMBBELL_STEP_UP', 'reps'),
    (dumbbell_step_up_hold_generator, 'DUMBBELL_STEP_UP', 'hold'),
    (dumbbell_stepover_rep_generator, 'DUMBBELL_STEPOVER', 'reps'),
    (dumbbell_stepover_hold_generator, 'DUMBBELL_STEPOVER', 'hold'),
    (dumbbell_thrusters_rep_generator, 'DUMBBELL_THRUSTERS', 'reps'),
    (dumbbell_thrusters_hold_generator, 'DUMBBELL_THRUSTERS', 'hold'),
    (elevated_single_leg_squat_rep_generator, 'ELEVATED_SINGLE_LEG_SQUAT', 'reps'),
    (elevated_single_leg_squat_hold_generator, 'ELEVATED_SINGLE_LEG_SQUAT', 'hold'),
    (figure_four_squats_rep_generator, 'FIGURE_FOUR_SQUATS', 'reps'),
    (figure_four_squats_hold_generator, 'FIGURE_FOUR_SQUATS', 'hold'),
    (goblet_squat_rep_generator, 'GOBLET_SQUAT', 'reps'),
    (goblet_squat_hold_generator, 'GOBLET_SQUAT', 'hold'),
    (kettlebell_squat_rep_generator, 'KETTLEBELL_SQUAT', 'reps'),
    (kettlebell_squat_hold_generator, 'KETTLEBELL_SQUAT', 'hold'),
    (kettlebell_swing_overhead_rep_generator, 'KETTLEBELL_SWING_OVERHEAD', 'reps'),
    (kettlebell_swing_overhead_hold_generator, 'KETTLEBELL_SWING_OVERHEAD', 'hold'),
    (kettlebell_swing_with_flip_to_squat_rep_generator, 'KETTLEBELL_SWING_WITH_FLIP_TO_SQUAT', 'reps'),
    (kettlebell_swing_with_flip_to_squat_hold_generator, 'KETTLEBELL_SWING_WITH_FLIP_TO_SQUAT', 'hold'),
    (lateral_dumbbell_step_up_rep_generator, 'LATERAL_DUMBBELL_STEP_UP', 'reps'),
    (lateral_dumbbell_step_up_hold_generator, 'LATERAL_DUMBBELL_STEP_UP', 'hold'),
    (leg_press_rep_generator, 'LEG_PRESS', 'reps'),
    (leg_press_hold_generator, 'LEG_PRESS', 'hold'),
    (medicine_ball_squat_rep_generator, 'MEDICINE_BALL_SQUAT', 'reps'),
    (medicine_ball_squat_hold_generator, 'MEDICINE_BALL_SQUAT', 'hold'),
    (one_legged_squat_rep_generator, 'ONE_LEGGED_SQUAT', 'reps'),
    (one_legged_squat_hold_generator, 'ONE_LEGGED_SQUAT', 'hold'),
    (overhead_barbell_squat_rep_generator, 'OVERHEAD_BARBELL_SQUAT', 'reps'),
    (overhead_barbell_squat_hold_generator, 'OVERHEAD_BARBELL_SQUAT', 'hold'),
    (overhead_dumbbell_squat_rep_generator, 'OVERHEAD_DUMBBELL_SQUAT', 'reps'),
    (overhead_dumbbell_squat_hold_generator, 'OVERHEAD_DUMBBELL_SQUAT', 'hold'),
    (overhead_squat_rep_generator, 'OVERHEAD_SQUAT', 'reps'),
    (overhead_squat_hold_generator, 'OVERHEAD_SQUAT', 'hold'),
    (partial_single_leg_squat_rep_generator, 'PARTIAL_SINGLE_LEG_SQUAT', 'reps'),
    (partial_single_leg_squat_hold_generator, 'PARTIAL_SINGLE_LEG_SQUAT', 'hold'),
    (pistol_squat_rep_generator, 'PISTOL_SQUAT', 'reps'),
    (pistol_squat_hold_generator, 'PISTOL_SQUAT', 'hold'),
    (plie_slides_rep_generator, 'PLIE_SLIDES', 'reps'),
    (plie_slides_hold_generator, 'PLIE_SLIDES', 'hold'),
    (plie_squat_rep_generator, 'PLIE_SQUAT', 'reps'),
    (plie_squat_hold_generator, 'PLIE_SQUAT', 'hold'),
    (prisoner_squat_rep_generator, 'PRISONER_SQUAT', 'reps'),
    (prisoner_squat_hold_generator, 'PRISONER_SQUAT', 'hold'),
    (single_leg_bench_get_up_rep_generator, 'SINGLE_LEG_BENCH_GET_UP', 'reps'),
    (single_leg_bench_get_up_hold_generator, 'SINGLE_LEG_BENCH_GET_UP', 'hold'),
    (single_leg_bench_squat_rep_generator, 'SINGLE_LEG_BENCH_SQUAT', 'reps'),
    (single_leg_bench_squat_hold_generator, 'SINGLE_LEG_BENCH_SQUAT', 'hold'),
    (single_leg_squat_on_swiss_ball_rep_generator, 'SINGLE_LEG_SQUAT_ON_SWISS_BALL', 'reps'),
    (single_leg_squat_on_swiss_ball_hold_generator, 'SINGLE_LEG_SQUAT_ON_SWISS_BALL', 'hold'),
    (squat_rep_generator, 'SQUAT', 'reps'),
    (squat_hold_generator, 'SQUAT', 'hold'),
    (squat_american_swing_rep_generator, 'SQUAT_AMERICAN_SWING', 'reps'),
    (squat_american_swing_hold_generator, 'SQUAT_AMERICAN_SWING', 'hold'),
    (squat_and_side_kick_rep_generator, 'SQUAT_AND_SIDE_KICK', 'reps'),
    (squat_and_side_kick_hold_generator, 'SQUAT_AND_SIDE_KICK', 'hold'),
    (squat_jumps_in_n_out_rep_generator, 'SQUAT_JUMPS_IN_N_OUT', 'reps'),
    (squat_jumps_in_n_out_hold_generator, 'SQUAT_JUMPS_IN_N_OUT', 'hold'),
    (squats_with_band_rep_generator, 'SQUATS_WITH_BAND', 'reps'),
    (squats_with_band_hold_generator, 'SQUATS_WITH_BAND', 'hold'),
    (staggered_squat_rep_generator, 'STAGGERED_SQUAT', 'reps'),
    (staggered_squat_hold_generator, 'STAGGERED_SQUAT', 'hold'),
    (step_up_rep_generator, 'STEP_UP', 'reps'),
    (step_up_hold_generator, 'STEP_UP', 'hold'),
    (suitcase_squats_rep_generator, 'SUITCASE_SQUATS', 'reps'),
    (suitcase_squats_hold_generator, 'SUITCASE_SQUATS', 'hold'),
    (sumo_squat_rep_generator, 'SUMO_SQUAT', 'reps'),
    (sumo_squat_hold_generator, 'SUMO_SQUAT', 'hold'),
    (sumo_squat_slide_in_rep_generator, 'SUMO_SQUAT_SLIDE_IN', 'reps'),
    (sumo_squat_slide_in_hold_generator, 'SUMO_SQUAT_SLIDE_IN', 'hold'),
    (sumo_squat_to_high_pull_rep_generator, 'SUMO_SQUAT_TO_HIGH_PULL', 'reps'),
    (sumo_squat_to_high_pull_hold_generator, 'SUMO_SQUAT_TO_HIGH_PULL', 'hold'),
    (sumo_squat_to_stand_rep_generator, 'SUMO_SQUAT_TO_STAND', 'reps'),
    (sumo_squat_to_stand_hold_generator, 'SUMO_SQUAT_TO_STAND', 'hold'),
    (sumo_squat_with_rotation_rep_generator, 'SUMO_SQUAT_WITH_ROTATION', 'reps'),
    (sumo_squat_with_rotation_hold_generator, 'SUMO_SQUAT_WITH_ROTATION', 'hold'),
    (swiss_ball_body_weight_wall_squat_rep_generator, 'SWISS_BALL_BODY_WEIGHT_WALL_SQUAT', 'reps'),
    (swiss_ball_body_weight_wall_squat_hold_generator, 'SWISS_BALL_BODY_WEIGHT_WALL_SQUAT', 'hold'),
    (thrusters_rep_generator, 'THRUSTERS', 'reps'),
    (thrusters_hold_generator, 'THRUSTERS', 'hold'),
    (uneven_squat_rep_generator, 'UNEVEN_SQUAT', 'reps'),
    (uneven_squat_hold_generator, 'UNEVEN_SQUAT', 'hold'),
    (waist_slimming_squat_rep_generator, 'WAIST_SLIMMING_SQUAT', 'reps'),
    (waist_slimming_squat_hold_generator, 'WAIST_SLIMMING_SQUAT', 'hold'),
    (wall_ball_rep_generator, 'WALL_BALL', 'reps'),
    (wall_ball_hold_generator, 'WALL_BALL', 'hold'),
    (wall_ball_squat_and_press_rep_generator, 'WALL_BALL_SQUAT_AND_PRESS', 'reps'),
    (wall_ball_squat_and_press_hold_generator, 'WALL_BALL_SQUAT_AND_PRESS', 'hold'),
    (weighted_back_squats_rep_generator, 'WEIGHTED_BACK_SQUATS', 'reps'),
    (weighted_back_squats_hold_generator, 'WEIGHTED_BACK_SQUATS', 'hold'),
    (weighted_balancing_squat_rep_generator, 'WEIGHTED_BALANCING_SQUAT', 'reps'),
    (weighted_balancing_squat_hold_generator, 'WEIGHTED_BALANCING_SQUAT', 'hold'),
    (weighted_bench_squat_with_rotational_chop_rep_generator, 'WEIGHTED_BENCH_SQUAT_WITH_ROTATIONAL_CHOP', 'reps'),
    (weighted_bench_squat_with_rotational_chop_hold_generator, 'WEIGHTED_BENCH_SQUAT_WITH_ROTATIONAL_CHOP', 'hold'),
    (weighted_box_step_squat_rep_generator, 'WEIGHTED_BOX_STEP_SQUAT', 'reps'),
    (weighted_box_step_squat_hold_generator, 'WEIGHTED_BOX_STEP_SQUAT', 'hold'),
    (weighted_elevated_single_leg_squat_rep_generator, 'WEIGHTED_ELEVATED_SINGLE_LEG_SQUAT', 'reps'),
    (weighted_elevated_single_leg_squat_hold_generator, 'WEIGHTED_ELEVATED_SINGLE_LEG_SQUAT', 'hold'),
    (weighted_figure_four_squats_rep_generator, 'WEIGHTED_FIGURE_FOUR_SQUATS', 'reps'),
    (weighted_figure_four_squats_hold_generator, 'WEIGHTED_FIGURE_FOUR_SQUATS', 'hold'),
    (weighted_partial_single_leg_squat_rep_generator, 'WEIGHTED_PARTIAL_SINGLE_LEG_SQUAT', 'reps'),
    (weighted_partial_single_leg_squat_hold_generator, 'WEIGHTED_PARTIAL_SINGLE_LEG_SQUAT', 'hold'),
    (weighted_pistol_squat_rep_generator, 'WEIGHTED_PISTOL_SQUAT', 'reps'),
    (weighted_pistol_squat_hold_generator, 'WEIGHTED_PISTOL_SQUAT', 'hold'),
    (weighted_plie_slides_rep_generator, 'WEIGHTED_PLIE_SLIDES', 'reps'),
    (weighted_plie_slides_hold_generator, 'WEIGHTED_PLIE_SLIDES', 'hold'),
    (weighted_plie_squat_rep_generator, 'WEIGHTED_PLIE_SQUAT', 'reps'),
    (weighted_plie_squat_hold_generator, 'WEIGHTED_PLIE_SQUAT', 'hold'),
    (weighted_prisoner_squat_rep_generator, 'WEIGHTED_PRISONER_SQUAT', 'reps'),
    (weighted_prisoner_squat_hold_generator, 'WEIGHTED_PRISONER_SQUAT', 'hold'),
    (weighted_single_leg_bench_get_up_rep_generator, 'WEIGHTED_SINGLE_LEG_BENCH_GET_UP', 'reps'),
    (weighted_single_leg_bench_get_up_hold_generator, 'WEIGHTED_SINGLE_LEG_BENCH_GET_UP', 'hold'),
    (weighted_single_leg_bench_squat_rep_generator, 'WEIGHTED_SINGLE_LEG_BENCH_SQUAT', 'reps'),
    (weighted_single_leg_bench_squat_hold_generator, 'WEIGHTED_SINGLE_LEG_BENCH_SQUAT', 'hold'),
    (weighted_single_leg_squat_on_swiss_ball_rep_generator, 'WEIGHTED_SINGLE_LEG_SQUAT_ON_SWISS_BALL', 'reps'),
    (weighted_single_leg_squat_on_swiss_ball_hold_generator, 'WEIGHTED_SINGLE_LEG_SQUAT_ON_SWISS_BALL', 'hold'),
    (weighted_squat_rep_generator, 'WEIGHTED_SQUAT', 'reps'),
    (weighted_squat_hold_generator, 'WEIGHTED_SQUAT', 'hold'),
    (weighted_staggered_squat_rep_generator, 'WEIGHTED_STAGGERED_SQUAT', 'reps'),
    (weighted_staggered_squat_hold_generator, 'WEIGHTED_STAGGERED_SQUAT', 'hold'),
    (weighted_step_up_rep_generator, 'WEIGHTED_STEP_UP', 'reps'),
    (weighted_step_up_hold_generator, 'WEIGHTED_STEP_UP', 'hold'),
    (weighted_sumo_squat_slide_in_rep_generator, 'WEIGHTED_SUMO_SQUAT_SLIDE_IN', 'reps'),
    (weighted_sumo_squat_slide_in_hold_generator, 'WEIGHTED_SUMO_SQUAT_SLIDE_IN', 'hold'),
    (weighted_sumo_squat_to_stand_rep_generator, 'WEIGHTED_SUMO_SQUAT_TO_STAND', 'reps'),
    (weighted_sumo_squat_to_stand_hold_generator, 'WEIGHTED_SUMO_SQUAT_TO_STAND', 'hold'),
    (weighted_sumo_squat_with_rotation_rep_generator, 'WEIGHTED_SUMO_SQUAT_WITH_ROTATION', 'reps'),
    (weighted_sumo_squat_with_rotation_hold_generator, 'WEIGHTED_SUMO_SQUAT_WITH_ROTATION', 'hold'),
    (weighted_swiss_ball_wall_squat_rep_generator, 'WEIGHTED_SWISS_BALL_WALL_SQUAT', 'reps'),
    (weighted_swiss_ball_wall_squat_hold_generator, 'WEIGHTED_SWISS_BALL_WALL_SQUAT', 'hold'),
    (weighted_uneven_squat_rep_generator, 'WEIGHTED_UNEVEN_SQUAT', 'reps'),
    (weighted_uneven_squat_hold_generator, 'WEIGHTED_UNEVEN_SQUAT', 'hold'),
    (weighted_wall_squat_rep_generator, 'WEIGHTED_WALL_SQUAT', 'reps'),
    (weighted_wall_squat_hold_generator, 'WEIGHTED_WALL_SQUAT', 'hold'),
    (wide_stance_barbell_squat_rep_generator, 'WIDE_STANCE_BARBELL_SQUAT', 'reps'),
    (wide_stance_barbell_squat_hold_generator, 'WIDE_STANCE_BARBELL_SQUAT', 'hold'),
    (wide_stance_goblet_squat_rep_generator, 'WIDE_STANCE_GOBLET_SQUAT', 'reps'),
    (wide_stance_goblet_squat_hold_generator, 'WIDE_STANCE_GOBLET_SQUAT', 'hold'),
    (zercher_squat_rep_generator, 'ZERCHER_SQUAT', 'reps'),
    (zercher_squat_hold_generator, 'ZERCHER_SQUAT', 'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'SQUAT'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
