import unittest

from garminworkouts.models.fields import _UNIT_KEY
from garminworkouts.models.workoutstep import WorkoutStep


class TestWorkoutStep(unittest.TestCase):
    def test_end_condition_unit(self) -> None:
        assert WorkoutStep.end_condition_unit('1km') == {_UNIT_KEY: 'kilometer'}
        assert WorkoutStep.end_condition_unit('1cals') == {_UNIT_KEY: 'calories'}
        assert WorkoutStep.end_condition_unit('1') == {_UNIT_KEY: None}
        assert WorkoutStep.end_condition_unit(None) is None

        assert WorkoutStep.parsed_end_condition_value('0:40') == 40
        assert WorkoutStep.parsed_end_condition_value('4:20') == 260
        assert WorkoutStep.parsed_end_condition_value('2.0km') == 2000
        assert WorkoutStep.parsed_end_condition_value('1.125km') == 1125
        assert WorkoutStep.parsed_end_condition_value('1.6km') == 1600
        assert WorkoutStep.parsed_end_condition_value('1cals') == 1
        assert WorkoutStep.parsed_end_condition_value('0ppm') == 0
        assert WorkoutStep.parsed_end_condition_value('0tp') == 0
        assert WorkoutStep.parsed_end_condition_value('10reps') == 10
        assert WorkoutStep.parsed_end_condition_value(None) == 0

        assert WorkoutStep._str_to_meters('2.0km') == 2000
        assert WorkoutStep._str_to_meters('1.125km') == 1125
        assert WorkoutStep._str_to_meters('1.6km') == 1600
        assert WorkoutStep._str_to_meters('500m') == 500
        assert WorkoutStep._str_to_meters('100m') == 100
        assert WorkoutStep._str_to_meters('10m') == 10
        assert WorkoutStep._str_to_meters('1m') == 1
        assert WorkoutStep._str_to_meters('0m') == 0
        assert WorkoutStep._str_to_meters('2km') == 2000
        assert WorkoutStep._str_to_meters('1.5km') == 1500
        assert WorkoutStep._str_to_meters('0.5km') == 500
