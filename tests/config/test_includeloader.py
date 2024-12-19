import unittest
from unittest.mock import patch
from garminworkouts.config.includeloader import generator_struct
import garminworkouts.config.generators.running as running
import garminworkouts.config.generators.strength as strength


class TestGeneratorStruct(unittest.TestCase):

    def setUp(self):
        self.running_patches = [
            patch.object(running.simple_step, 'R0_step_generator', return_value={'step': 'R0'}),
            patch.object(running.simple_step, 'R1_step_generator', return_value={'step': 'R1'}),
            patch.object(running.simple_step, 'R1p_step_generator', return_value={'step': 'R1p'}),
            patch.object(running.simple_step, 'R2_step_generator', return_value={'step': 'R2'}),
            patch.object(running.simple_step, 'R3_step_generator', return_value={'step': 'R3'}),
            patch.object(running.simple_step, 'R3p_step_generator', return_value={'step': 'R3p'}),
            patch.object(running.simple_step, 'R4_step_generator', return_value={'step': 'R4'}),
            patch.object(running.simple_step, 'R5_step_generator', return_value={'step': 'R5'}),
            patch.object(running.simple_step, 'R6_step_generator', return_value={'step': 'R6'}),
            patch.object(running.multi_step, 'Rseries_generator', return_value={'step': 'intervals'}),
            patch.object(running.simple_step, 'recovery_step_generator', return_value={'step': 'recovery'}),
            patch.object(running.simple_step, 'aerobic_step_generator', return_value={'step': 'aerobic'}),
            patch.object(running.simple_step, 'lt_step_generator', return_value={'step': 'lt'}),
            patch.object(running.simple_step, 'lr_step_generator', return_value={'step': 'lr'}),
            patch.object(running.simple_step, 'marathon_step_generator', return_value={'step': 'marathon'}),
            patch.object(running.simple_step, 'hm_step_generator', return_value={'step': 'hm'}),
            patch.object(running.simple_step, 'tuneup_step_generator', return_value={'step': 'tuneup'}),
            patch.object(running.simple_step, 'warmup_step_generator', return_value={'step': 'warmup'}),
            patch.object(running.simple_step, 'cooldown_step_generator', return_value={'step': 'cooldown'}),
            patch.object(running.simple_step, 'walk_step_generator', return_value={'step': 'walk'}),
            patch.object(running.multi_step, 'stride_generator', return_value={'step': 'stride'}),
            patch.object(running.multi_step, 'longhill_generator', return_value={'step': 'longhill'}),
            patch.object(running.multi_step, 'hill_generator', return_value={'step': 'hill'}),
            patch.object(running.multi_step, 'acceleration_generator', return_value={'step': 'acceleration'}),
            patch.object(running.multi_step, 'series_generator', return_value={'step': 'series'}),
            patch.object(running.multi_step, 'anaerobic_generator', return_value={'step': 'anaerobic'}),
            patch.object(running.multi_step, 'race_generator', return_value={'step': 'race'}),
        ]
        self.strength_patches = [
            patch.object(strength.multi_step, 'plank_push_hold_generator', return_value={'step': 'PlankPushHold'}),
            patch.object(strength.multi_step, 'plank_push_angel_generator', return_value={'step': 'PlankPushAngel'}),
            patch.object(strength.multi_step, 'calf_hold_lunge_generator', return_value={'step': 'CalfHoldLunge'}),
            patch.object(strength.multi_step, 'calf_lunge_side_generator', return_value={'step': 'CalfLungeSide'}),
            patch.object(strength.multi_step, 'calf_lunge_squat_generator', return_value={'step': 'CalfLungeSquat'}),
            patch.object(strength.multi_step, 'calf_squat_hold_generator', return_value={'step': 'CalfSquatHold'}),
            patch.object(strength.multi_step, 'climber_shoulder_tap_plank_rot_generator',
                         return_value={'step': 'ClimberShouldertapPlankrot'}),
            patch.object(strength.multi_step, 'calf_hold_squat_generator', return_value={'step': 'CalfHoldSquat'}),
            patch.object(strength.multi_step, 'leg_raise_hold_situp_generator',
                         return_value={'step': 'LegRaiseHoldSitup'}),
            patch.object(strength.multi_step, 'leg_raise_hold_kneetwist_generator',
                         return_value={'step': 'LegRaiseHoldSKneetwist'}),
            patch.object(strength.multi_step, 'max_pushups_generator', return_value={'step': 'MaxPushups'}),
            patch.object(strength.multi_step, 'shoulder_tap_updown_plank_hold_generator',
                         return_value={'step': 'ShoulderTapUpdownPlankHold'}),
            patch.object(strength.multi_step, 'flutter_kick_circle_high_crunch_generator',
                         return_value={'step': 'FlutterKickCrunch'}),
            patch.object(strength.multi_step, 'plank_rotation_walkout_altraises_generator',
                         return_value={'step': 'PlankRotationWalkOutAltRaises'}),
        ]

        for p in self.running_patches + self.strength_patches:
            p.start()
            self.addCleanup(p.stop)

    def test_generator_struct(self):
        self.assertEqual(generator_struct('test', '10min', 0, 'R0'), {'step': 'R0'})
        self.assertEqual(generator_struct('test', '10min', 0, 'R1'), {'step': 'R1'})
        self.assertEqual(generator_struct('test', '10min', 0, 'R1p'), {'step': 'R1p'})
        self.assertEqual(generator_struct('test', '10min', 0, 'R2'), {'step': 'R2'})
        self.assertEqual(generator_struct('test', '10min', 0, 'R3'), {'step': 'R3'})
        self.assertEqual(generator_struct('test', '10min', 0, 'R3p'), {'step': 'R3p'})
        self.assertEqual(generator_struct('test', '10min', 0, 'R4'), {'step': 'R4'})
        self.assertEqual(generator_struct('test', '10min', 0, 'R5'), {'step': 'R5'})
        self.assertEqual(generator_struct('test', '10min', 0, 'R6'), {'step': 'R6'})
        self.assertEqual(generator_struct('test', '10min', 0, 'intervals'), {'step': 'intervals'})
        self.assertEqual(generator_struct('test', '10min', 0, 'recovery'), {'step': 'recovery'})
        self.assertEqual(generator_struct('test', '10min', 0, 'aerobic'), {'step': 'aerobic'})
        self.assertEqual(generator_struct('test', '10min', 0, 'lt'), {'step': 'lt'})
        self.assertEqual(generator_struct('test', '10min', 0, 'lr'), {'step': 'lr'})
        self.assertEqual(generator_struct('test', '10min', 0, 'marathon'), {'step': 'marathon'})
        self.assertEqual(generator_struct('test', '10min', 0, 'hm'), {'step': 'hm'})
        self.assertEqual(generator_struct('test', '10min', 0, 'tuneup'), {'step': 'tuneup'})
        self.assertEqual(generator_struct('test', '10min', 0, 'warmup'), {'step': 'warmup'})
        self.assertEqual(generator_struct('test', '10min', 0, 'cooldown'), {'step': 'cooldown'})
        self.assertEqual(generator_struct('test', '10min', 0, 'walk'), {'step': 'walk'})
        self.assertEqual(generator_struct('test', '10min', 0, 'stride'), {'step': 'stride'})
        self.assertEqual(generator_struct('test', '10min', 0, 'longhill'), {'step': 'longhill'})
        self.assertEqual(generator_struct('test', '10min', 0, 'hill'), {'step': 'hill'})
        self.assertEqual(generator_struct('test', '10min', 0, 'acceleration'), {'step': 'acceleration'})
        self.assertEqual(generator_struct('test', '10min', 0, 'series'), {'step': 'series'})
        self.assertEqual(generator_struct('test', '10min', 0, 'anaerobic'), {'step': 'anaerobic'})
        self.assertEqual(generator_struct('test', '10min', 0, 'race'), {'step': 'race'})
        self.assertEqual(generator_struct('test', '10min', 0, 'PlankPushHold'), {'step': 'PlankPushHold'})
        self.assertEqual(generator_struct('test', '10min', 0, 'PlankPushAngel'), {'step': 'PlankPushAngel'})
        self.assertEqual(generator_struct('test', '10min', 0, 'CalfHoldLunge'), {'step': 'CalfHoldLunge'})
        self.assertEqual(generator_struct('test', '10min', 0, 'CalfLungeSide'), {'step': 'CalfLungeSide'})
        self.assertEqual(generator_struct('test', '10min', 0, 'CalfLungeSquat'), {'step': 'CalfLungeSquat'})
        self.assertEqual(generator_struct('test', '10min', 0, 'CalfSquatHold'), {'step': 'CalfSquatHold'})
        self.assertEqual(generator_struct('test', '10min', 0, 'ClimberShouldertapPlankrot'),
                         {'step': 'ClimberShouldertapPlankrot'})
        self.assertEqual(generator_struct('test', '10min', 0, 'CalfHoldSquat'), {'step': 'CalfHoldSquat'})
        self.assertEqual(generator_struct('test', '10min', 0, 'LegRaiseHoldSitup'), {'step': 'LegRaiseHoldSitup'})
        self.assertEqual(generator_struct('test', '10min', 0, 'LegRaiseHoldSKneetwist'),
                         {'step': 'LegRaiseHoldSKneetwist'})
        self.assertEqual(generator_struct('test', '10min', 0, 'MaxPushups'), {'step': 'MaxPushups'})
        self.assertEqual(generator_struct('test', '10min', 0, 'ShoulderTapUpdownPlankHold'),
                         {'step': 'ShoulderTapUpdownPlankHold'})
        self.assertEqual(generator_struct('test', '10min', 0, 'FlutterKickCrunch'), {'step': 'FlutterKickCrunch'})
        self.assertEqual(generator_struct('test', '10min', 0, 'PlankRotationWalkOutAltRaises'),
                         {'step': 'PlankRotationWalkOutAltRaises'})
        self.assertEqual(generator_struct('test', '10min', 0, 'NonExistentStep'), {})
