from tests.trainingplans.base_test import BaseTest
from trainingplans.lists import NikeLists


class TrainingPlanTestCase(BaseTest):
    def test_trainingplan_nike_marathon(self) -> None:
        self.check_workout_files(NikeLists)
