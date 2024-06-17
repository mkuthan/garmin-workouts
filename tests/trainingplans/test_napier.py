from tests.trainingplans.base_test import BaseTest
from trainingplans.lists import NapierLists


class TrainingPlanTestCase(BaseTest):
    def test_trainingplan_napier(self) -> None:
        self.check_workout_files(NapierLists)
