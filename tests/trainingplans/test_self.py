from tests.trainingplans.base_test import BaseTest
from trainingplans.lists import SelfLists


class TrainingPlanTestCase(BaseTest):
    def test_trainingplan_self(self) -> None:
        self.check_workout_files(SelfLists)
