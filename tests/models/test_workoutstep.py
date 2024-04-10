import unittest

from garminworkouts.models.fields import _UNIT_KEY
from garminworkouts.models.workoutstep import WorkoutStep


class TestWorkoutStep(unittest.TestCase):
    def test_end_condition_unit(self) -> None:
        assert WorkoutStep.end_condition_unit('1km') == {_UNIT_KEY: 'kilometer'}
        assert WorkoutStep.end_condition_unit('1cals') == {_UNIT_KEY: 'calories'}
        assert WorkoutStep.end_condition_unit('1') == {_UNIT_KEY: None}
        assert WorkoutStep.end_condition_unit(None) is None
