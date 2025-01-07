import unittest
from unittest.mock import patch, mock_open
from garminworkouts.config.includeloader import (IncludeLoader, camel_to_snake, extract_duration, generator_struct,
                                                 step_generator)
import os
import yaml
import garminworkouts.config.generators.strength as strength
import garminworkouts.config.generators.running as running


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

    def test_step_generator(self):
        self.assertEqual(step_generator('R0', '10min', 0), {'step': 'R0'})
        self.assertEqual(step_generator('R1', '10min', 0), {'step': 'R1'})
        self.assertEqual(step_generator('R1p', '10min', 0), {'step': 'R1p'})
        self.assertEqual(step_generator('R2', '10min', 0), {'step': 'R2'})
        self.assertEqual(step_generator('R3', '10min', 0), {'step': 'R3'})
        self.assertEqual(step_generator('R3p', '10min', 0), {'step': 'R3p'})
        self.assertEqual(step_generator('R4', '10min', 0), {'step': 'R4'})
        self.assertEqual(step_generator('R5', '10min', 0), {'step': 'R5'})
        self.assertEqual(step_generator('R6', '10min', 0), {'step': 'R6'})
        self.assertEqual(step_generator('intervals', '10min', 0), {'step': 'intervals'})
        self.assertEqual(step_generator('recovery', '10min', 0), {'step': 'recovery'})
        self.assertEqual(step_generator('aerobic', '10min', 0), {'step': 'aerobic'})
        self.assertEqual(step_generator('lt', '10min', 0), {'step': 'lt'})
        self.assertEqual(step_generator('lr', '10min', 0), {'step': 'lr'})
        self.assertEqual(step_generator('marathon', '10min', 0), {'step': 'marathon'})
        self.assertEqual(step_generator('hm', '10min', 0), {'step': 'hm'})
        self.assertEqual(step_generator('tuneup', '10min', 0), {'step': 'tuneup'})
        self.assertEqual(step_generator('warmup', '10min', 0), {'step': 'warmup'})
        self.assertEqual(step_generator('cooldown', '10min', 0), {'step': 'cooldown'})
        self.assertEqual(step_generator('walk', '10min', 0), {'step': 'walk'})
        self.assertEqual(step_generator('stride', '10min', 0), {'step': 'stride'})
        self.assertEqual(step_generator('longhill', '10min', 0), {'step': 'longhill'})
        self.assertEqual(step_generator('hill', '10min', 0), {'step': 'hill'})
        self.assertEqual(step_generator('acceleration', '10min', 0), {'step': 'acceleration'})
        self.assertEqual(step_generator('series', '10min', 0), {'step': 'series'})
        self.assertEqual(step_generator('anaerobic', '10min', 0), {'step': 'anaerobic'})
        self.assertEqual(step_generator('race', '10min', 0), {'step': 'race'})
        self.assertEqual(step_generator('PlankPushHold', '10min', 0), {'step': 'PlankPushHold'})
        self.assertEqual(step_generator('PlankPushAngel', '10min', 0), {'step': 'PlankPushAngel'})
        self.assertEqual(step_generator('CalfHoldLunge', '10min', 0), {'step': 'CalfHoldLunge'})
        self.assertEqual(step_generator('CalfLungeSide', '10min', 0), {'step': 'CalfLungeSide'})
        self.assertEqual(step_generator('CalfLungeSquat', '10min', 0), {'step': 'CalfLungeSquat'})
        self.assertEqual(step_generator('CalfSquatHold', '10min', 0), {'step': 'CalfSquatHold'})
        self.assertEqual(step_generator('ClimberShouldertapPlankrot', '10min', 0),
                         {'step': 'ClimberShouldertapPlankrot'})
        self.assertEqual(step_generator('CalfHoldSquat', '10min', 0), {'step': 'CalfHoldSquat'})
        self.assertEqual(step_generator('LegRaiseHoldSitup', '10min', 0), {'step': 'LegRaiseHoldSitup'})
        self.assertEqual(step_generator('LegRaiseHoldSKneetwist', '10min', 0), {'step': 'LegRaiseHoldSKneetwist'})
        self.assertEqual(step_generator('MaxPushups', '10min', 0), {'step': 'MaxPushups'})
        self.assertEqual(step_generator('ShoulderTapUpdownPlankHold', '10min', 0),
                         {'step': 'ShoulderTapUpdownPlankHold'})
        self.assertEqual(step_generator('FlutterKickCrunch', '10min', 0), {'step': 'FlutterKickCrunch'})
        self.assertEqual(step_generator('PlankRotationWalkOutAltRaises', '10min', 0),
                         {'step': 'PlankRotationWalkOutAltRaises'})
        self.assertEqual(step_generator('NonExistentStep', '10min', 0), {})


class TestExtractDuration(unittest.TestCase):
    def test_extract_duration_minutes(self):
        self.assertEqual(extract_duration('10min'), '0:10:00')
        self.assertEqual(extract_duration('5.5min'), '0:05:30')

    def test_extract_duration_seconds(self):
        self.assertEqual(extract_duration('30s'), '0:00:30')
        self.assertEqual(extract_duration('90s'), '0:01:30')

    def test_extract_duration_reps(self):
        self.assertEqual(extract_duration('15reps'), '15')

    def test_extract_duration_colon_format(self):
        self.assertEqual(extract_duration('00:30:00'), '00:30:00')

    def test_extract_duration_km(self):
        self.assertEqual(extract_duration('5km'), '5km')

    def test_extract_duration_mile(self):
        self.assertEqual(extract_duration('1mile'), '1.609km')
        self.assertEqual(extract_duration('2mile'), '3.218km')

    def test_extract_duration_meters(self):
        self.assertEqual(extract_duration('500m'), '500m')

    def test_extract_duration_k(self):
        self.assertEqual(extract_duration('10k'), '10km')

    def test_extract_duration_half(self):
        self.assertEqual(extract_duration('half'), '21.1km')

    def test_extract_duration_default(self):
        self.assertEqual(extract_duration('3,5'), '3.5km')
        self.assertEqual(extract_duration('4.2'), '4.2km')


class TestIncludeLoader(unittest.TestCase):

    def setUp(self):
        self.loader = IncludeLoader

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data="test: data")
    @patch('yaml.load')
    def test_include_file_exists(self, mock_yaml_load, mock_open, mock_isfile):
        mock_isfile.return_value = True
        mock_yaml_load.return_value = {'test': 'data'}

        node = yaml.ScalarNode(tag='!include', value='test.yaml')
        mock_file = mock_open(read_data="")
        mock_file.name = 'mocked_file.yaml'
        loader_instance = self.loader(stream=mock_file)
        result = loader_instance.include(node)

        mock_open.assert_called_with(os.path.join(loader_instance._root, 'test.yaml'), 'r')
        mock_yaml_load.assert_called_with(mock_open(), IncludeLoader)
        self.assertEqual(result, {'test': 'data'})

    @patch('builtins.open', new_callable=mock_open)
    def test_include_file_not_exists1(self, mock_open):
        filename = 'inntervals-R09-R1_10min_5min_sub3.yaml'
        node = yaml.ScalarNode(tag='!include', value=filename)
        mock_file = mock_open(read_data="")
        mock_file.name = filename
        mock_file.read = lambda size=None: ''
        loader_instance = self.loader(stream=mock_file)
        result = loader_instance.include(node)
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_include_file_not_exists2(self, mock_open):
        filename = 'inntervals_xmin.yaml'
        node = yaml.ScalarNode(tag='!include', value=filename)
        mock_file = mock_open(read_data="")
        mock_file.name = filename
        mock_file.read = lambda size=None: ''
        loader_instance = self.loader(stream=mock_file)
        result = loader_instance.include(node)
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_include_file_not_exists3(self, mock_open):
        filename = 'anerobic_x.yaml'
        node = yaml.ScalarNode(tag='!include', value=filename)
        mock_file = mock_open(read_data="")
        mock_file.name = filename
        mock_file.read = lambda size=None: ''
        loader_instance = self.loader(stream=mock_file)
        result = loader_instance.include(node)
        self.assertEqual(result, {})


class TestCamelToSnake(unittest.TestCase):
    def test_camel_to_snake(self):
        self.assertEqual(camel_to_snake('CamelCase'), 'camel_case')
        self.assertEqual(camel_to_snake('camelCase'), 'camel_case')
        self.assertEqual(camel_to_snake('CamelCamelCase'), 'camel_camel_case')
        self.assertEqual(camel_to_snake('Camel2Camel2Case'), 'camel2_camel2_case')
        self.assertEqual(camel_to_snake('getHTTPResponseCode'), 'get_http_response_code')
        self.assertEqual(camel_to_snake('get2HTTPResponseCode'), 'get2_http_response_code')
        self.assertEqual(camel_to_snake('HTTPResponseCode'), 'http_response_code')
        self.assertEqual(camel_to_snake('HTTPResponseCodeXYZ'), 'http_response_code_xyz')
