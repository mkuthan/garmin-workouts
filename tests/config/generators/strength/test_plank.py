import pytest

from garminworkouts.config.generators.strength.plank import (
    _45_degree_plank_rep_generator,
    _45_degree_plank_hold_generator,
    _90_degree_static_hold_rep_generator,
    _90_degree_static_hold_hold_generator,
    bear_crawl_rep_generator,
    bear_crawl_hold_generator,
    cross_body_mountain_climber_rep_generator,
    cross_body_mountain_climber_hold_generator,
    elbow_plank_pike_jacks_rep_generator,
    elbow_plank_pike_jacks_hold_generator,
    elevated_feet_plank_rep_generator,
    elevated_feet_plank_hold_generator,
    elevator_abs_rep_generator,
    elevator_abs_hold_generator,
    extended_plank_rep_generator,
    extended_plank_hold_generator,
    full_plank_passe_twist_rep_generator,
    full_plank_passe_twist_hold_generator,
    inching_elbow_plank_rep_generator,
    inching_elbow_plank_hold_generator,
    inchworm_to_side_plank_rep_generator,
    inchworm_to_side_plank_hold_generator,
    kneeling_plank_rep_generator,
    kneeling_plank_hold_generator,
    kneeling_side_plank_with_leg_lift_rep_generator,
    kneeling_side_plank_with_leg_lift_hold_generator,
    lateral_roll_rep_generator,
    lateral_roll_hold_generator,
    lying_reverse_plank_rep_generator,
    lying_reverse_plank_hold_generator,
    medicine_ball_mountain_climber_rep_generator,
    medicine_ball_mountain_climber_hold_generator,
    modified_mountain_climber_and_extension_rep_generator,
    modified_mountain_climber_and_extension_hold_generator,
    mountain_climber_rep_generator,
    mountain_climber_hold_generator,
    mountain_climber_on_sliding_discs_rep_generator,
    mountain_climber_on_sliding_discs_hold_generator,
    mountain_climber_with_feet_on_bosu_ball_rep_generator,
    mountain_climber_with_feet_on_bosu_ball_hold_generator,
    mountain_climber_with_hands_on_bench_rep_generator,
    mountain_climber_with_hands_on_bench_hold_generator,
    mountain_climber_with_hands_on_swiss_ball_rep_generator,
    mountain_climber_with_hands_on_swiss_ball_hold_generator,
    plank_rep_generator,
    plank_hold_generator,
    plank_jacks_with_feet_on_sliding_discs_rep_generator,
    plank_jacks_with_feet_on_sliding_discs_hold_generator,
    plank_knee_twist_rep_generator,
    plank_knee_twist_hold_generator,
    plank_pike_jumps_rep_generator,
    plank_pike_jumps_hold_generator,
    plank_pikes_rep_generator,
    plank_pikes_hold_generator,
    plank_to_stand_up_rep_generator,
    plank_to_stand_up_hold_generator,
    plank_with_arm_raise_rep_generator,
    plank_with_arm_raise_hold_generator,
    plank_with_feet_on_swiss_ball_rep_generator,
    plank_with_feet_on_swiss_ball_hold_generator,
    plank_with_knee_to_elbow_rep_generator,
    plank_with_knee_to_elbow_hold_generator,
    plank_with_leg_lift_rep_generator,
    plank_with_leg_lift_hold_generator,
    plank_with_oblique_crunch_rep_generator,
    plank_with_oblique_crunch_hold_generator,
    plyometric_side_plank_rep_generator,
    plyometric_side_plank_hold_generator,
    ring_plank_sprawls_rep_generator,
    ring_plank_sprawls_hold_generator,
    rolling_side_plank_rep_generator,
    rolling_side_plank_hold_generator,
    side_kick_plank_rep_generator,
    side_kick_plank_hold_generator,
    side_plank_rep_generator,
    side_plank_hold_generator,
    side_plank_and_row_rep_generator,
    side_plank_and_row_hold_generator,
    side_plank_lift_rep_generator,
    side_plank_lift_hold_generator,
    side_plank_to_plank_with_reach_under_rep_generator,
    side_plank_to_plank_with_reach_under_hold_generator,
    side_plank_with_elbow_on_bosu_ball_rep_generator,
    side_plank_with_elbow_on_bosu_ball_hold_generator,
    side_plank_with_feet_on_bench_rep_generator,
    side_plank_with_feet_on_bench_hold_generator,
    side_plank_with_knee_circle_rep_generator,
    side_plank_with_knee_circle_hold_generator,
    side_plank_with_knee_tuck_rep_generator,
    side_plank_with_knee_tuck_hold_generator,
    side_plank_with_leg_lift_rep_generator,
    side_plank_with_leg_lift_hold_generator,
    side_plank_with_reach_under_rep_generator,
    side_plank_with_reach_under_hold_generator,
    single_leg_elevated_feet_plank_rep_generator,
    single_leg_elevated_feet_plank_hold_generator,
    single_leg_flex_and_extend_rep_generator,
    single_leg_flex_and_extend_hold_generator,
    single_leg_side_plank_rep_generator,
    single_leg_side_plank_hold_generator,
    spiderman_plank_rep_generator,
    spiderman_plank_hold_generator,
    straight_arm_plank_rep_generator,
    straight_arm_plank_hold_generator,
    straight_arm_plank_with_shoulder_touch_rep_generator,
    straight_arm_plank_with_shoulder_touch_hold_generator,
    swiss_ball_plank_rep_generator,
    swiss_ball_plank_hold_generator,
    swiss_ball_plank_leg_lift_rep_generator,
    swiss_ball_plank_leg_lift_hold_generator,
    swiss_ball_plank_leg_lift_and_hold_rep_generator,
    swiss_ball_plank_leg_lift_and_hold_hold_generator,
    swiss_ball_plank_with_feet_on_bench_rep_generator,
    swiss_ball_plank_with_feet_on_bench_hold_generator,
    swiss_ball_prone_jackknife_rep_generator,
    swiss_ball_prone_jackknife_hold_generator,
    swiss_ball_side_plank_rep_generator,
    swiss_ball_side_plank_hold_generator,
    t_stabilization_rep_generator,
    t_stabilization_hold_generator,
    three_way_plank_rep_generator,
    three_way_plank_hold_generator,
    towel_plank_and_knee_in_rep_generator,
    towel_plank_and_knee_in_hold_generator,
    turkish_get_up_to_side_plank_rep_generator,
    turkish_get_up_to_side_plank_hold_generator,
    two_point_plank_rep_generator,
    two_point_plank_hold_generator,
    weighted_45_degree_plank_rep_generator,
    weighted_45_degree_plank_hold_generator,
    weighted_90_degree_static_hold_rep_generator,
    weighted_90_degree_static_hold_hold_generator,
    weighted_bear_crawl_rep_generator,
    weighted_bear_crawl_hold_generator,
    weighted_cross_body_mountain_climber_rep_generator,
    weighted_cross_body_mountain_climber_hold_generator,
    weighted_elbow_plank_pike_jacks_rep_generator,
    weighted_elbow_plank_pike_jacks_hold_generator,
    weighted_elevated_feet_plank_rep_generator,
    weighted_elevated_feet_plank_hold_generator,
    weighted_elevator_abs_rep_generator,
    weighted_elevator_abs_hold_generator,
    weighted_extended_plank_rep_generator,
    weighted_extended_plank_hold_generator,
    weighted_full_plank_passe_twist_rep_generator,
    weighted_full_plank_passe_twist_hold_generator,
    weighted_inching_elbow_plank_rep_generator,
    weighted_inching_elbow_plank_hold_generator,
    weighted_inchworm_to_side_plank_rep_generator,
    weighted_inchworm_to_side_plank_hold_generator,
    weighted_kneeling_plank_rep_generator,
    weighted_kneeling_plank_hold_generator,
    weighted_kneeling_side_plank_with_leg_lift_rep_generator,
    weighted_kneeling_side_plank_with_leg_lift_hold_generator,
    weighted_lateral_roll_rep_generator,
    weighted_lateral_roll_hold_generator,
    weighted_lying_reverse_plank_rep_generator,
    weighted_lying_reverse_plank_hold_generator,
    weighted_medicine_ball_mountain_climber_rep_generator,
    weighted_medicine_ball_mountain_climber_hold_generator,
    weighted_modified_mountain_climber_and_extension_rep_generator,
    weighted_modified_mountain_climber_and_extension_hold_generator,
    weighted_mountain_climber_rep_generator,
    weighted_mountain_climber_hold_generator,
    weighted_mountain_climber_on_sliding_discs_rep_generator,
    weighted_mountain_climber_on_sliding_discs_hold_generator,
    weighted_mountain_climber_with_feet_on_bosu_ball_rep_generator,
    weighted_mountain_climber_with_feet_on_bosu_ball_hold_generator,
    weighted_mountain_climber_with_hands_on_bench_rep_generator,
    weighted_mountain_climber_with_hands_on_bench_hold_generator,
    weighted_mountain_climber_with_hands_on_swiss_ball_rep_generator,
    weighted_mountain_climber_with_hands_on_swiss_ball_hold_generator,
    weighted_plank_rep_generator,
    weighted_plank_hold_generator,
    weighted_plank_jacks_with_feet_on_sliding_discs_rep_generator,
    weighted_plank_jacks_with_feet_on_sliding_discs_hold_generator,
    weighted_plank_knee_twist_rep_generator,
    weighted_plank_knee_twist_hold_generator,
    weighted_plank_pike_jumps_rep_generator,
    weighted_plank_pike_jumps_hold_generator,
    weighted_plank_pikes_rep_generator,
    weighted_plank_pikes_hold_generator,
    weighted_plank_to_stand_up_rep_generator,
    weighted_plank_to_stand_up_hold_generator,
    weighted_plank_with_arm_raise_rep_generator,
    weighted_plank_with_arm_raise_hold_generator,
    weighted_plank_with_knee_to_elbow_rep_generator,
    weighted_plank_with_knee_to_elbow_hold_generator,
    weighted_plank_with_oblique_crunch_rep_generator,
    weighted_plank_with_oblique_crunch_hold_generator,
    weighted_plyometric_side_plank_rep_generator,
    weighted_plyometric_side_plank_hold_generator,
    weighted_rolling_side_plank_rep_generator,
    weighted_rolling_side_plank_hold_generator,
    weighted_side_kick_plank_rep_generator,
    weighted_side_kick_plank_hold_generator,
    weighted_side_plank_rep_generator,
    weighted_side_plank_hold_generator,
    weighted_side_plank_and_row_rep_generator,
    weighted_side_plank_and_row_hold_generator,
    weighted_side_plank_lift_rep_generator,
    weighted_side_plank_lift_hold_generator,
    weighted_side_plank_with_elbow_on_bosu_ball_rep_generator,
    weighted_side_plank_with_elbow_on_bosu_ball_hold_generator,
    weighted_side_plank_with_feet_on_bench_rep_generator,
    weighted_side_plank_with_feet_on_bench_hold_generator,
    weighted_side_plank_with_knee_circle_rep_generator,
    weighted_side_plank_with_knee_circle_hold_generator,
    weighted_side_plank_with_knee_tuck_rep_generator,
    weighted_side_plank_with_knee_tuck_hold_generator,
    weighted_side_plank_with_leg_lift_rep_generator,
    weighted_side_plank_with_leg_lift_hold_generator,
    weighted_side_plank_with_reach_under_rep_generator,
    weighted_side_plank_with_reach_under_hold_generator,
    weighted_single_leg_elevated_feet_plank_rep_generator,
    weighted_single_leg_elevated_feet_plank_hold_generator,
    weighted_single_leg_flex_and_extend_rep_generator,
    weighted_single_leg_flex_and_extend_hold_generator,
    weighted_single_leg_side_plank_rep_generator,
    weighted_single_leg_side_plank_hold_generator,
    weighted_spiderman_plank_rep_generator,
    weighted_spiderman_plank_hold_generator,
    weighted_straight_arm_plank_rep_generator,
    weighted_straight_arm_plank_hold_generator,
    weighted_straight_arm_plank_with_shoulder_touch_rep_generator,
    weighted_straight_arm_plank_with_shoulder_touch_hold_generator,
    weighted_swiss_ball_plank_rep_generator,
    weighted_swiss_ball_plank_hold_generator,
    weighted_swiss_ball_plank_leg_lift_rep_generator,
    weighted_swiss_ball_plank_leg_lift_hold_generator,
    weighted_swiss_ball_plank_leg_lift_and_hold_rep_generator,
    weighted_swiss_ball_plank_leg_lift_and_hold_hold_generator,
    weighted_swiss_ball_plank_with_feet_on_bench_rep_generator,
    weighted_swiss_ball_plank_with_feet_on_bench_hold_generator,
    weighted_swiss_ball_prone_jackknife_rep_generator,
    weighted_swiss_ball_prone_jackknife_hold_generator,
    weighted_swiss_ball_side_plank_rep_generator,
    weighted_swiss_ball_side_plank_hold_generator,
    weighted_t_stabilization_rep_generator,
    weighted_t_stabilization_hold_generator,
    weighted_three_way_plank_rep_generator,
    weighted_three_way_plank_hold_generator,
    weighted_towel_plank_and_knee_in_rep_generator,
    weighted_towel_plank_and_knee_in_hold_generator,
    weighted_turkish_get_up_to_side_plank_rep_generator,
    weighted_turkish_get_up_to_side_plank_hold_generator,
    weighted_two_point_plank_rep_generator,
    weighted_two_point_plank_hold_generator,
    weighted_wide_stance_plank_with_diagonal_arm_lift_rep_generator,
    weighted_wide_stance_plank_with_diagonal_arm_lift_hold_generator,
    weighted_wide_stance_plank_with_diagonal_leg_lift_rep_generator,
    weighted_wide_stance_plank_with_diagonal_leg_lift_hold_generator,
    weighted_wide_stance_plank_with_leg_lift_rep_generator,
    weighted_wide_stance_plank_with_leg_lift_hold_generator,
    wide_stance_plank_with_diagonal_arm_lift_rep_generator,
    wide_stance_plank_with_diagonal_arm_lift_hold_generator,
    wide_stance_plank_with_diagonal_leg_lift_rep_generator,
    wide_stance_plank_with_diagonal_leg_lift_hold_generator,
    wide_stance_plank_with_leg_lift_rep_generator,
    wide_stance_plank_with_leg_lift_hold_generator,
    wide_stance_plank_with_opposite_arm_and_leg_lift_rep_generator,
    wide_stance_plank_with_opposite_arm_and_leg_lift_hold_generator,
    )


@pytest.mark.parametrize("generator, exercise_name, execution", [
    (_45_degree_plank_rep_generator, '_45_DEGREE_PLANK', 'reps'),
    (_45_degree_plank_hold_generator, '_45_DEGREE_PLANK', 'hold'),
    (_90_degree_static_hold_rep_generator, '_90_DEGREE_STATIC_HOLD', 'reps'),
    (_90_degree_static_hold_hold_generator, '_90_DEGREE_STATIC_HOLD', 'hold'),
    (bear_crawl_rep_generator, 'BEAR_CRAWL', 'reps'),
    (bear_crawl_hold_generator, 'BEAR_CRAWL', 'hold'),
    (cross_body_mountain_climber_rep_generator, 'CROSS_BODY_MOUNTAIN_CLIMBER', 'reps'),
    (cross_body_mountain_climber_hold_generator, 'CROSS_BODY_MOUNTAIN_CLIMBER', 'hold'),
    (elbow_plank_pike_jacks_rep_generator, 'ELBOW_PLANK_PIKE_JACKS', 'reps'),
    (elbow_plank_pike_jacks_hold_generator, 'ELBOW_PLANK_PIKE_JACKS', 'hold'),
    (elevated_feet_plank_rep_generator, 'ELEVATED_FEET_PLANK', 'reps'),
    (elevated_feet_plank_hold_generator, 'ELEVATED_FEET_PLANK', 'hold'),
    (elevator_abs_rep_generator, 'ELEVATOR_ABS', 'reps'),
    (elevator_abs_hold_generator, 'ELEVATOR_ABS', 'hold'),
    (extended_plank_rep_generator, 'EXTENDED_PLANK', 'reps'),
    (extended_plank_hold_generator, 'EXTENDED_PLANK', 'hold'),
    (full_plank_passe_twist_rep_generator, 'FULL_PLANK_PASSE_TWIST', 'reps'),
    (full_plank_passe_twist_hold_generator, 'FULL_PLANK_PASSE_TWIST', 'hold'),
    (inching_elbow_plank_rep_generator, 'INCHING_ELBOW_PLANK', 'reps'),
    (inching_elbow_plank_hold_generator, 'INCHING_ELBOW_PLANK', 'hold'),
    (inchworm_to_side_plank_rep_generator, 'INCHWORM_TO_SIDE_PLANK', 'reps'),
    (inchworm_to_side_plank_hold_generator, 'INCHWORM_TO_SIDE_PLANK', 'hold'),
    (kneeling_plank_rep_generator, 'KNEELING_PLANK', 'reps'),
    (kneeling_plank_hold_generator, 'KNEELING_PLANK', 'hold'),
    (kneeling_side_plank_with_leg_lift_rep_generator, 'KNEELING_SIDE_PLANK_WITH_LEG_LIFT', 'reps'),
    (kneeling_side_plank_with_leg_lift_hold_generator, 'KNEELING_SIDE_PLANK_WITH_LEG_LIFT', 'hold'),
    (lateral_roll_rep_generator, 'LATERAL_ROLL', 'reps'),
    (lateral_roll_hold_generator, 'LATERAL_ROLL', 'hold'),
    (lying_reverse_plank_rep_generator, 'LYING_REVERSE_PLANK', 'reps'),
    (lying_reverse_plank_hold_generator, 'LYING_REVERSE_PLANK', 'hold'),
    (medicine_ball_mountain_climber_rep_generator, 'MEDICINE_BALL_MOUNTAIN_CLIMBER', 'reps'),
    (medicine_ball_mountain_climber_hold_generator, 'MEDICINE_BALL_MOUNTAIN_CLIMBER', 'hold'),
    (modified_mountain_climber_and_extension_rep_generator, 'MODIFIED_MOUNTAIN_CLIMBER_AND_EXTENSION', 'reps'),
    (modified_mountain_climber_and_extension_hold_generator, 'MODIFIED_MOUNTAIN_CLIMBER_AND_EXTENSION', 'hold'),
    (mountain_climber_rep_generator, 'MOUNTAIN_CLIMBER', 'reps'),
    (mountain_climber_hold_generator, 'MOUNTAIN_CLIMBER', 'hold'),
    (mountain_climber_on_sliding_discs_rep_generator, 'MOUNTAIN_CLIMBER_ON_SLIDING_DISCS', 'reps'),
    (mountain_climber_on_sliding_discs_hold_generator, 'MOUNTAIN_CLIMBER_ON_SLIDING_DISCS', 'hold'),
    (mountain_climber_with_feet_on_bosu_ball_rep_generator, 'MOUNTAIN_CLIMBER_WITH_FEET_ON_BOSU_BALL', 'reps'),
    (mountain_climber_with_feet_on_bosu_ball_hold_generator, 'MOUNTAIN_CLIMBER_WITH_FEET_ON_BOSU_BALL', 'hold'),
    (mountain_climber_with_hands_on_bench_rep_generator, 'MOUNTAIN_CLIMBER_WITH_HANDS_ON_BENCH', 'reps'),
    (mountain_climber_with_hands_on_bench_hold_generator, 'MOUNTAIN_CLIMBER_WITH_HANDS_ON_BENCH', 'hold'),
    (mountain_climber_with_hands_on_swiss_ball_rep_generator, 'MOUNTAIN_CLIMBER_WITH_HANDS_ON_SWISS_BALL', 'reps'),
    (mountain_climber_with_hands_on_swiss_ball_hold_generator, 'MOUNTAIN_CLIMBER_WITH_HANDS_ON_SWISS_BALL', 'hold'),
    (plank_rep_generator, 'PLANK', 'reps'),
    (plank_hold_generator, 'PLANK', 'hold'),
    (plank_jacks_with_feet_on_sliding_discs_rep_generator, 'PLANK_JACKS_WITH_FEET_ON_SLIDING_DISCS', 'reps'),
    (plank_jacks_with_feet_on_sliding_discs_hold_generator, 'PLANK_JACKS_WITH_FEET_ON_SLIDING_DISCS', 'hold'),
    (plank_knee_twist_rep_generator, 'PLANK_KNEE_TWIST', 'reps'),
    (plank_knee_twist_hold_generator, 'PLANK_KNEE_TWIST', 'hold'),
    (plank_pike_jumps_rep_generator, 'PLANK_PIKE_JUMPS', 'reps'),
    (plank_pike_jumps_hold_generator, 'PLANK_PIKE_JUMPS', 'hold'),
    (plank_pikes_rep_generator, 'PLANK_PIKES', 'reps'),
    (plank_pikes_hold_generator, 'PLANK_PIKES', 'hold'),
    (plank_to_stand_up_rep_generator, 'PLANK_TO_STAND_UP', 'reps'),
    (plank_to_stand_up_hold_generator, 'PLANK_TO_STAND_UP', 'hold'),
    (plank_with_arm_raise_rep_generator, 'PLANK_WITH_ARM_RAISE', 'reps'),
    (plank_with_arm_raise_hold_generator, 'PLANK_WITH_ARM_RAISE', 'hold'),
    (plank_with_feet_on_swiss_ball_rep_generator, 'PLANK_WITH_FEET_ON_SWISS_BALL', 'reps'),
    (plank_with_feet_on_swiss_ball_hold_generator, 'PLANK_WITH_FEET_ON_SWISS_BALL', 'hold'),
    (plank_with_knee_to_elbow_rep_generator, 'PLANK_WITH_KNEE_TO_ELBOW', 'reps'),
    (plank_with_knee_to_elbow_hold_generator, 'PLANK_WITH_KNEE_TO_ELBOW', 'hold'),
    (plank_with_leg_lift_rep_generator, 'PLANK_WITH_LEG_LIFT', 'reps'),
    (plank_with_leg_lift_hold_generator, 'PLANK_WITH_LEG_LIFT', 'hold'),
    (plank_with_oblique_crunch_rep_generator, 'PLANK_WITH_OBLIQUE_CRUNCH', 'reps'),
    (plank_with_oblique_crunch_hold_generator, 'PLANK_WITH_OBLIQUE_CRUNCH', 'hold'),
    (plyometric_side_plank_rep_generator, 'PLYOMETRIC_SIDE_PLANK', 'reps'),
    (plyometric_side_plank_hold_generator, 'PLYOMETRIC_SIDE_PLANK', 'hold'),
    (ring_plank_sprawls_rep_generator, 'RING_PLANK_SPRAWLS', 'reps'),
    (ring_plank_sprawls_hold_generator, 'RING_PLANK_SPRAWLS', 'hold'),
    (rolling_side_plank_rep_generator, 'ROLLING_SIDE_PLANK', 'reps'),
    (rolling_side_plank_hold_generator, 'ROLLING_SIDE_PLANK', 'hold'),
    (side_kick_plank_rep_generator, 'SIDE_KICK_PLANK', 'reps'),
    (side_kick_plank_hold_generator, 'SIDE_KICK_PLANK', 'hold'),
    (side_plank_rep_generator, 'SIDE_PLANK', 'reps'),
    (side_plank_hold_generator, 'SIDE_PLANK', 'hold'),
    (side_plank_and_row_rep_generator, 'SIDE_PLANK_AND_ROW', 'reps'),
    (side_plank_and_row_hold_generator, 'SIDE_PLANK_AND_ROW', 'hold'),
    (side_plank_lift_rep_generator, 'SIDE_PLANK_LIFT', 'reps'),
    (side_plank_lift_hold_generator, 'SIDE_PLANK_LIFT', 'hold'),
    (side_plank_to_plank_with_reach_under_rep_generator, 'SIDE_PLANK_TO_PLANK_WITH_REACH_UNDER', 'reps'),
    (side_plank_to_plank_with_reach_under_hold_generator, 'SIDE_PLANK_TO_PLANK_WITH_REACH_UNDER', 'hold'),
    (side_plank_with_elbow_on_bosu_ball_rep_generator, 'SIDE_PLANK_WITH_ELBOW_ON_BOSU_BALL', 'reps'),
    (side_plank_with_elbow_on_bosu_ball_hold_generator, 'SIDE_PLANK_WITH_ELBOW_ON_BOSU_BALL', 'hold'),
    (side_plank_with_feet_on_bench_rep_generator, 'SIDE_PLANK_WITH_FEET_ON_BENCH', 'reps'),
    (side_plank_with_feet_on_bench_hold_generator, 'SIDE_PLANK_WITH_FEET_ON_BENCH', 'hold'),
    (side_plank_with_knee_circle_rep_generator, 'SIDE_PLANK_WITH_KNEE_CIRCLE', 'reps'),
    (side_plank_with_knee_circle_hold_generator, 'SIDE_PLANK_WITH_KNEE_CIRCLE', 'hold'),
    (side_plank_with_knee_tuck_rep_generator, 'SIDE_PLANK_WITH_KNEE_TUCK', 'reps'),
    (side_plank_with_knee_tuck_hold_generator, 'SIDE_PLANK_WITH_KNEE_TUCK', 'hold'),
    (side_plank_with_leg_lift_rep_generator, 'SIDE_PLANK_WITH_LEG_LIFT', 'reps'),
    (side_plank_with_leg_lift_hold_generator, 'SIDE_PLANK_WITH_LEG_LIFT', 'hold'),
    (side_plank_with_reach_under_rep_generator, 'SIDE_PLANK_WITH_REACH_UNDER', 'reps'),
    (side_plank_with_reach_under_hold_generator, 'SIDE_PLANK_WITH_REACH_UNDER', 'hold'),
    (single_leg_elevated_feet_plank_rep_generator, 'SINGLE_LEG_ELEVATED_FEET_PLANK', 'reps'),
    (single_leg_elevated_feet_plank_hold_generator, 'SINGLE_LEG_ELEVATED_FEET_PLANK', 'hold'),
    (single_leg_flex_and_extend_rep_generator, 'SINGLE_LEG_FLEX_AND_EXTEND', 'reps'),
    (single_leg_flex_and_extend_hold_generator, 'SINGLE_LEG_FLEX_AND_EXTEND', 'hold'),
    (single_leg_side_plank_rep_generator, 'SINGLE_LEG_SIDE_PLANK', 'reps'),
    (single_leg_side_plank_hold_generator, 'SINGLE_LEG_SIDE_PLANK', 'hold'),
    (spiderman_plank_rep_generator, 'SPIDERMAN_PLANK', 'reps'),
    (spiderman_plank_hold_generator, 'SPIDERMAN_PLANK', 'hold'),
    (straight_arm_plank_rep_generator, 'STRAIGHT_ARM_PLANK', 'reps'),
    (straight_arm_plank_hold_generator, 'STRAIGHT_ARM_PLANK', 'hold'),
    (straight_arm_plank_with_shoulder_touch_rep_generator, 'STRAIGHT_ARM_PLANK_WITH_SHOULDER_TOUCH', 'reps'),
    (straight_arm_plank_with_shoulder_touch_hold_generator, 'STRAIGHT_ARM_PLANK_WITH_SHOULDER_TOUCH', 'hold'),
    (swiss_ball_plank_rep_generator, 'SWISS_BALL_PLANK', 'reps'),
    (swiss_ball_plank_hold_generator, 'SWISS_BALL_PLANK', 'hold'),
    (swiss_ball_plank_leg_lift_rep_generator, 'SWISS_BALL_PLANK_LEG_LIFT', 'reps'),
    (swiss_ball_plank_leg_lift_hold_generator, 'SWISS_BALL_PLANK_LEG_LIFT', 'hold'),
    (swiss_ball_plank_leg_lift_and_hold_rep_generator, 'SWISS_BALL_PLANK_LEG_LIFT_AND_HOLD', 'reps'),
    (swiss_ball_plank_leg_lift_and_hold_hold_generator, 'SWISS_BALL_PLANK_LEG_LIFT_AND_HOLD', 'hold'),
    (swiss_ball_plank_with_feet_on_bench_rep_generator, 'SWISS_BALL_PLANK_WITH_FEET_ON_BENCH', 'reps'),
    (swiss_ball_plank_with_feet_on_bench_hold_generator, 'SWISS_BALL_PLANK_WITH_FEET_ON_BENCH', 'hold'),
    (swiss_ball_prone_jackknife_rep_generator, 'SWISS_BALL_PRONE_JACKKNIFE', 'reps'),
    (swiss_ball_prone_jackknife_hold_generator, 'SWISS_BALL_PRONE_JACKKNIFE', 'hold'),
    (swiss_ball_side_plank_rep_generator, 'SWISS_BALL_SIDE_PLANK', 'reps'),
    (swiss_ball_side_plank_hold_generator, 'SWISS_BALL_SIDE_PLANK', 'hold'),
    (t_stabilization_rep_generator, 'T_STABILIZATION', 'reps'),
    (t_stabilization_hold_generator, 'T_STABILIZATION', 'hold'),
    (three_way_plank_rep_generator, 'THREE_WAY_PLANK', 'reps'),
    (three_way_plank_hold_generator, 'THREE_WAY_PLANK', 'hold'),
    (towel_plank_and_knee_in_rep_generator, 'TOWEL_PLANK_AND_KNEE_IN', 'reps'),
    (towel_plank_and_knee_in_hold_generator, 'TOWEL_PLANK_AND_KNEE_IN', 'hold'),
    (turkish_get_up_to_side_plank_rep_generator, 'TURKISH_GET_UP_TO_SIDE_PLANK', 'reps'),
    (turkish_get_up_to_side_plank_hold_generator, 'TURKISH_GET_UP_TO_SIDE_PLANK', 'hold'),
    (two_point_plank_rep_generator, 'TWO_POINT_PLANK', 'reps'),
    (two_point_plank_hold_generator, 'TWO_POINT_PLANK', 'hold'),
    (weighted_45_degree_plank_rep_generator, 'WEIGHTED_45_DEGREE_PLANK', 'reps'),
    (weighted_45_degree_plank_hold_generator, 'WEIGHTED_45_DEGREE_PLANK', 'hold'),
    (weighted_90_degree_static_hold_rep_generator, 'WEIGHTED_90_DEGREE_STATIC_HOLD', 'reps'),
    (weighted_90_degree_static_hold_hold_generator, 'WEIGHTED_90_DEGREE_STATIC_HOLD', 'hold'),
    (weighted_bear_crawl_rep_generator, 'WEIGHTED_BEAR_CRAWL', 'reps'),
    (weighted_bear_crawl_hold_generator, 'WEIGHTED_BEAR_CRAWL', 'hold'),
    (weighted_cross_body_mountain_climber_rep_generator, 'WEIGHTED_CROSS_BODY_MOUNTAIN_CLIMBER', 'reps'),
    (weighted_cross_body_mountain_climber_hold_generator, 'WEIGHTED_CROSS_BODY_MOUNTAIN_CLIMBER', 'hold'),
    (weighted_elbow_plank_pike_jacks_rep_generator, 'WEIGHTED_ELBOW_PLANK_PIKE_JACKS', 'reps'),
    (weighted_elbow_plank_pike_jacks_hold_generator, 'WEIGHTED_ELBOW_PLANK_PIKE_JACKS', 'hold'),
    (weighted_elevated_feet_plank_rep_generator, 'WEIGHTED_ELEVATED_FEET_PLANK', 'reps'),
    (weighted_elevated_feet_plank_hold_generator, 'WEIGHTED_ELEVATED_FEET_PLANK', 'hold'),
    (weighted_elevator_abs_rep_generator, 'WEIGHTED_ELEVATOR_ABS', 'reps'),
    (weighted_elevator_abs_hold_generator, 'WEIGHTED_ELEVATOR_ABS', 'hold'),
    (weighted_extended_plank_rep_generator, 'WEIGHTED_EXTENDED_PLANK', 'reps'),
    (weighted_extended_plank_hold_generator, 'WEIGHTED_EXTENDED_PLANK', 'hold'),
    (weighted_full_plank_passe_twist_rep_generator, 'WEIGHTED_FULL_PLANK_PASSE_TWIST', 'reps'),
    (weighted_full_plank_passe_twist_hold_generator, 'WEIGHTED_FULL_PLANK_PASSE_TWIST', 'hold'),
    (weighted_inching_elbow_plank_rep_generator, 'WEIGHTED_INCHING_ELBOW_PLANK', 'reps'),
    (weighted_inching_elbow_plank_hold_generator, 'WEIGHTED_INCHING_ELBOW_PLANK', 'hold'),
    (weighted_inchworm_to_side_plank_rep_generator, 'WEIGHTED_INCHWORM_TO_SIDE_PLANK', 'reps'),
    (weighted_inchworm_to_side_plank_hold_generator, 'WEIGHTED_INCHWORM_TO_SIDE_PLANK', 'hold'),
    (weighted_kneeling_plank_rep_generator, 'WEIGHTED_KNEELING_PLANK', 'reps'),
    (weighted_kneeling_plank_hold_generator, 'WEIGHTED_KNEELING_PLANK', 'hold'),
    (weighted_kneeling_side_plank_with_leg_lift_rep_generator, 'WEIGHTED_KNEELING_SIDE_PLANK_WITH_LEG_LIFT', 'reps'),
    (weighted_kneeling_side_plank_with_leg_lift_hold_generator, 'WEIGHTED_KNEELING_SIDE_PLANK_WITH_LEG_LIFT', 'hold'),
    (weighted_lateral_roll_rep_generator, 'WEIGHTED_LATERAL_ROLL', 'reps'),
    (weighted_lateral_roll_hold_generator, 'WEIGHTED_LATERAL_ROLL', 'hold'),
    (weighted_lying_reverse_plank_rep_generator, 'WEIGHTED_LYING_REVERSE_PLANK', 'reps'),
    (weighted_lying_reverse_plank_hold_generator, 'WEIGHTED_LYING_REVERSE_PLANK', 'hold'),
    (weighted_medicine_ball_mountain_climber_rep_generator, 'WEIGHTED_MEDICINE_BALL_MOUNTAIN_CLIMBER', 'reps'),
    (weighted_medicine_ball_mountain_climber_hold_generator, 'WEIGHTED_MEDICINE_BALL_MOUNTAIN_CLIMBER', 'hold'),
    (weighted_modified_mountain_climber_and_extension_rep_generator, 'WEIGHTED_MODIFIED_MOUNTAIN_CLIMBER_AND_EXTENSION', 'reps'),
    (weighted_modified_mountain_climber_and_extension_hold_generator, 'WEIGHTED_MODIFIED_MOUNTAIN_CLIMBER_AND_EXTENSION', 'hold'),
    (weighted_mountain_climber_rep_generator, 'WEIGHTED_MOUNTAIN_CLIMBER', 'reps'),
    (weighted_mountain_climber_hold_generator, 'WEIGHTED_MOUNTAIN_CLIMBER', 'hold'),
    (weighted_mountain_climber_on_sliding_discs_rep_generator, 'WEIGHTED_MOUNTAIN_CLIMBER_ON_SLIDING_DISCS', 'reps'),
    (weighted_mountain_climber_on_sliding_discs_hold_generator, 'WEIGHTED_MOUNTAIN_CLIMBER_ON_SLIDING_DISCS', 'hold'),
    (weighted_mountain_climber_with_feet_on_bosu_ball_rep_generator, 'WEIGHTED_MOUNTAIN_CLIMBER_WITH_FEET_ON_BOSU_BALL', 'reps'),
    (weighted_mountain_climber_with_feet_on_bosu_ball_hold_generator, 'WEIGHTED_MOUNTAIN_CLIMBER_WITH_FEET_ON_BOSU_BALL', 'hold'),
    (weighted_mountain_climber_with_hands_on_bench_rep_generator, 'WEIGHTED_MOUNTAIN_CLIMBER_WITH_HANDS_ON_BENCH', 'reps'),
    (weighted_mountain_climber_with_hands_on_bench_hold_generator, 'WEIGHTED_MOUNTAIN_CLIMBER_WITH_HANDS_ON_BENCH', 'hold'),
    (weighted_mountain_climber_with_hands_on_swiss_ball_rep_generator, 'WEIGHTED_MOUNTAIN_CLIMBER_WITH_HANDS_ON_SWISS_BALL', 'reps'),
    (weighted_mountain_climber_with_hands_on_swiss_ball_hold_generator, 'WEIGHTED_MOUNTAIN_CLIMBER_WITH_HANDS_ON_SWISS_BALL', 'hold'),
    (weighted_plank_rep_generator, 'WEIGHTED_PLANK', 'reps'),
    (weighted_plank_hold_generator, 'WEIGHTED_PLANK', 'hold'),
    (weighted_plank_jacks_with_feet_on_sliding_discs_rep_generator, 'WEIGHTED_PLANK_JACKS_WITH_FEET_ON_SLIDING_DISCS', 'reps'),
    (weighted_plank_jacks_with_feet_on_sliding_discs_hold_generator, 'WEIGHTED_PLANK_JACKS_WITH_FEET_ON_SLIDING_DISCS', 'hold'),
    (weighted_plank_knee_twist_rep_generator, 'WEIGHTED_PLANK_KNEE_TWIST', 'reps'),
    (weighted_plank_knee_twist_hold_generator, 'WEIGHTED_PLANK_KNEE_TWIST', 'hold'),
    (weighted_plank_pike_jumps_rep_generator, 'WEIGHTED_PLANK_PIKE_JUMPS', 'reps'),
    (weighted_plank_pike_jumps_hold_generator, 'WEIGHTED_PLANK_PIKE_JUMPS', 'hold'),
    (weighted_plank_pikes_rep_generator, 'WEIGHTED_PLANK_PIKES', 'reps'),
    (weighted_plank_pikes_hold_generator, 'WEIGHTED_PLANK_PIKES', 'hold'),
    (weighted_plank_to_stand_up_rep_generator, 'WEIGHTED_PLANK_TO_STAND_UP', 'reps'),
    (weighted_plank_to_stand_up_hold_generator, 'WEIGHTED_PLANK_TO_STAND_UP', 'hold'),
    (weighted_plank_with_arm_raise_rep_generator, 'WEIGHTED_PLANK_WITH_ARM_RAISE', 'reps'),
    (weighted_plank_with_arm_raise_hold_generator, 'WEIGHTED_PLANK_WITH_ARM_RAISE', 'hold'),
    (weighted_plank_with_knee_to_elbow_rep_generator, 'WEIGHTED_PLANK_WITH_KNEE_TO_ELBOW', 'reps'),
    (weighted_plank_with_knee_to_elbow_hold_generator, 'WEIGHTED_PLANK_WITH_KNEE_TO_ELBOW', 'hold'),
    (weighted_plank_with_oblique_crunch_rep_generator, 'WEIGHTED_PLANK_WITH_OBLIQUE_CRUNCH', 'reps'),
    (weighted_plank_with_oblique_crunch_hold_generator, 'WEIGHTED_PLANK_WITH_OBLIQUE_CRUNCH', 'hold'),
    (weighted_plyometric_side_plank_rep_generator, 'WEIGHTED_PLYOMETRIC_SIDE_PLANK', 'reps'),
    (weighted_plyometric_side_plank_hold_generator, 'WEIGHTED_PLYOMETRIC_SIDE_PLANK', 'hold'),
    (weighted_rolling_side_plank_rep_generator, 'WEIGHTED_ROLLING_SIDE_PLANK', 'reps'),
    (weighted_rolling_side_plank_hold_generator, 'WEIGHTED_ROLLING_SIDE_PLANK', 'hold'),
    (weighted_side_kick_plank_rep_generator, 'WEIGHTED_SIDE_KICK_PLANK', 'reps'),
    (weighted_side_kick_plank_hold_generator, 'WEIGHTED_SIDE_KICK_PLANK', 'hold'),
    (weighted_side_plank_rep_generator, 'WEIGHTED_SIDE_PLANK', 'reps'),
    (weighted_side_plank_hold_generator, 'WEIGHTED_SIDE_PLANK', 'hold'),
    (weighted_side_plank_and_row_rep_generator, 'WEIGHTED_SIDE_PLANK_AND_ROW', 'reps'),
    (weighted_side_plank_and_row_hold_generator, 'WEIGHTED_SIDE_PLANK_AND_ROW', 'hold'),
    (weighted_side_plank_lift_rep_generator, 'WEIGHTED_SIDE_PLANK_LIFT', 'reps'),
    (weighted_side_plank_lift_hold_generator, 'WEIGHTED_SIDE_PLANK_LIFT', 'hold'),
    (weighted_side_plank_with_elbow_on_bosu_ball_rep_generator, 'WEIGHTED_SIDE_PLANK_WITH_ELBOW_ON_BOSU_BALL', 'reps'),
    (weighted_side_plank_with_elbow_on_bosu_ball_hold_generator, 'WEIGHTED_SIDE_PLANK_WITH_ELBOW_ON_BOSU_BALL', 'hold'),
    (weighted_side_plank_with_feet_on_bench_rep_generator, 'WEIGHTED_SIDE_PLANK_WITH_FEET_ON_BENCH', 'reps'),
    (weighted_side_plank_with_feet_on_bench_hold_generator, 'WEIGHTED_SIDE_PLANK_WITH_FEET_ON_BENCH', 'hold'),
    (weighted_side_plank_with_knee_circle_rep_generator, 'WEIGHTED_SIDE_PLANK_WITH_KNEE_CIRCLE', 'reps'),
    (weighted_side_plank_with_knee_circle_hold_generator, 'WEIGHTED_SIDE_PLANK_WITH_KNEE_CIRCLE', 'hold'),
    (weighted_side_plank_with_knee_tuck_rep_generator, 'WEIGHTED_SIDE_PLANK_WITH_KNEE_TUCK', 'reps'),
    (weighted_side_plank_with_knee_tuck_hold_generator, 'WEIGHTED_SIDE_PLANK_WITH_KNEE_TUCK', 'hold'),
    (weighted_side_plank_with_leg_lift_rep_generator, 'WEIGHTED_SIDE_PLANK_WITH_LEG_LIFT', 'reps'),
    (weighted_side_plank_with_leg_lift_hold_generator, 'WEIGHTED_SIDE_PLANK_WITH_LEG_LIFT', 'hold'),
    (weighted_side_plank_with_reach_under_rep_generator, 'WEIGHTED_SIDE_PLANK_WITH_REACH_UNDER', 'reps'),
    (weighted_side_plank_with_reach_under_hold_generator, 'WEIGHTED_SIDE_PLANK_WITH_REACH_UNDER', 'hold'),
    (weighted_single_leg_elevated_feet_plank_rep_generator, 'WEIGHTED_SINGLE_LEG_ELEVATED_FEET_PLANK', 'reps'),
    (weighted_single_leg_elevated_feet_plank_hold_generator, 'WEIGHTED_SINGLE_LEG_ELEVATED_FEET_PLANK', 'hold'),
    (weighted_single_leg_flex_and_extend_rep_generator, 'WEIGHTED_SINGLE_LEG_FLEX_AND_EXTEND', 'reps'),
    (weighted_single_leg_flex_and_extend_hold_generator, 'WEIGHTED_SINGLE_LEG_FLEX_AND_EXTEND', 'hold'),
    (weighted_single_leg_side_plank_rep_generator, 'WEIGHTED_SINGLE_LEG_SIDE_PLANK', 'reps'),
    (weighted_single_leg_side_plank_hold_generator, 'WEIGHTED_SINGLE_LEG_SIDE_PLANK', 'hold'),
    (weighted_spiderman_plank_rep_generator, 'WEIGHTED_SPIDERMAN_PLANK', 'reps'),
    (weighted_spiderman_plank_hold_generator, 'WEIGHTED_SPIDERMAN_PLANK', 'hold'),
    (weighted_straight_arm_plank_rep_generator, 'WEIGHTED_STRAIGHT_ARM_PLANK', 'reps'),
    (weighted_straight_arm_plank_hold_generator, 'WEIGHTED_STRAIGHT_ARM_PLANK', 'hold'),
    (weighted_straight_arm_plank_with_shoulder_touch_rep_generator, 'WEIGHTED_STRAIGHT_ARM_PLANK_WITH_SHOULDER_TOUCH', 'reps'),
    (weighted_straight_arm_plank_with_shoulder_touch_hold_generator, 'WEIGHTED_STRAIGHT_ARM_PLANK_WITH_SHOULDER_TOUCH', 'hold'),
    (weighted_swiss_ball_plank_rep_generator, 'WEIGHTED_SWISS_BALL_PLANK', 'reps'),
    (weighted_swiss_ball_plank_hold_generator, 'WEIGHTED_SWISS_BALL_PLANK', 'hold'),
    (weighted_swiss_ball_plank_leg_lift_rep_generator, 'WEIGHTED_SWISS_BALL_PLANK_LEG_LIFT', 'reps'),
    (weighted_swiss_ball_plank_leg_lift_hold_generator, 'WEIGHTED_SWISS_BALL_PLANK_LEG_LIFT', 'hold'),
    (weighted_swiss_ball_plank_leg_lift_and_hold_rep_generator, 'WEIGHTED_SWISS_BALL_PLANK_LEG_LIFT_AND_HOLD', 'reps'),
    (weighted_swiss_ball_plank_leg_lift_and_hold_hold_generator, 'WEIGHTED_SWISS_BALL_PLANK_LEG_LIFT_AND_HOLD', 'hold'),
    (weighted_swiss_ball_plank_with_feet_on_bench_rep_generator, 'WEIGHTED_SWISS_BALL_PLANK_WITH_FEET_ON_BENCH', 'reps'),
    (weighted_swiss_ball_plank_with_feet_on_bench_hold_generator, 'WEIGHTED_SWISS_BALL_PLANK_WITH_FEET_ON_BENCH', 'hold'),
    (weighted_swiss_ball_prone_jackknife_rep_generator, 'WEIGHTED_SWISS_BALL_PRONE_JACKKNIFE', 'reps'),
    (weighted_swiss_ball_prone_jackknife_hold_generator, 'WEIGHTED_SWISS_BALL_PRONE_JACKKNIFE', 'hold'),
    (weighted_swiss_ball_side_plank_rep_generator, 'WEIGHTED_SWISS_BALL_SIDE_PLANK', 'reps'),
    (weighted_swiss_ball_side_plank_hold_generator, 'WEIGHTED_SWISS_BALL_SIDE_PLANK', 'hold'),
    (weighted_t_stabilization_rep_generator, 'WEIGHTED_T_STABILIZATION', 'reps'),
    (weighted_t_stabilization_hold_generator, 'WEIGHTED_T_STABILIZATION', 'hold'),
    (weighted_three_way_plank_rep_generator, 'WEIGHTED_THREE_WAY_PLANK', 'reps'),
    (weighted_three_way_plank_hold_generator, 'WEIGHTED_THREE_WAY_PLANK', 'hold'),
    (weighted_towel_plank_and_knee_in_rep_generator, 'WEIGHTED_TOWEL_PLANK_AND_KNEE_IN', 'reps'),
    (weighted_towel_plank_and_knee_in_hold_generator, 'WEIGHTED_TOWEL_PLANK_AND_KNEE_IN', 'hold'),
    (weighted_turkish_get_up_to_side_plank_rep_generator, 'WEIGHTED_TURKISH_GET_UP_TO_SIDE_PLANK', 'reps'),
    (weighted_turkish_get_up_to_side_plank_hold_generator, 'WEIGHTED_TURKISH_GET_UP_TO_SIDE_PLANK', 'hold'),
    (weighted_two_point_plank_rep_generator, 'WEIGHTED_TWO_POINT_PLANK', 'reps'),
    (weighted_two_point_plank_hold_generator, 'WEIGHTED_TWO_POINT_PLANK', 'hold'),
    (weighted_wide_stance_plank_with_diagonal_arm_lift_rep_generator, 'WEIGHTED_WIDE_STANCE_PLANK_WITH_DIAGONAL_ARM_LIFT', 'reps'),
    (weighted_wide_stance_plank_with_diagonal_arm_lift_hold_generator, 'WEIGHTED_WIDE_STANCE_PLANK_WITH_DIAGONAL_ARM_LIFT', 'hold'),
    (weighted_wide_stance_plank_with_diagonal_leg_lift_rep_generator, 'WEIGHTED_WIDE_STANCE_PLANK_WITH_DIAGONAL_LEG_LIFT', 'reps'),
    (weighted_wide_stance_plank_with_diagonal_leg_lift_hold_generator, 'WEIGHTED_WIDE_STANCE_PLANK_WITH_DIAGONAL_LEG_LIFT', 'hold'),
    (weighted_wide_stance_plank_with_leg_lift_rep_generator, 'WEIGHTED_WIDE_STANCE_PLANK_WITH_LEG_LIFT', 'reps'),
    (weighted_wide_stance_plank_with_leg_lift_hold_generator, 'WEIGHTED_WIDE_STANCE_PLANK_WITH_LEG_LIFT', 'hold'),
    (wide_stance_plank_with_diagonal_arm_lift_rep_generator, 'WIDE_STANCE_PLANK_WITH_DIAGONAL_ARM_LIFT', 'reps'),
    (wide_stance_plank_with_diagonal_arm_lift_hold_generator, 'WIDE_STANCE_PLANK_WITH_DIAGONAL_ARM_LIFT', 'hold'),
    (wide_stance_plank_with_diagonal_leg_lift_rep_generator, 'WIDE_STANCE_PLANK_WITH_DIAGONAL_LEG_LIFT', 'reps'),
    (wide_stance_plank_with_diagonal_leg_lift_hold_generator, 'WIDE_STANCE_PLANK_WITH_DIAGONAL_LEG_LIFT', 'hold'),
    (wide_stance_plank_with_leg_lift_rep_generator, 'WIDE_STANCE_PLANK_WITH_LEG_LIFT', 'reps'),
    (wide_stance_plank_with_leg_lift_hold_generator, 'WIDE_STANCE_PLANK_WITH_LEG_LIFT', 'hold'),
    (wide_stance_plank_with_opposite_arm_and_leg_lift_rep_generator, 'WIDE_STANCE_PLANK_WITH_OPPOSITE_ARM_AND_LEG_LIFT', 'reps'),
    (wide_stance_plank_with_opposite_arm_and_leg_lift_hold_generator, 'WIDE_STANCE_PLANK_WITH_OPPOSITE_ARM_AND_LEG_LIFT', 'hold'),
    ])
def test_exercise_generators(generator, exercise_name, execution):
    duration = "10reps" if execution == 'reps' else 'lap.button'
    description = exercise_name.replace('_', ' ').title() if execution == 'reps' else "10-count hold"
    result = generator(10)
    assert result['category'] == 'PLANK'
    assert result['exerciseName'] == exercise_name
    assert result['duration'] == duration
    assert result['target'] == 'NO_TARGET'
    assert result['description'] == description
