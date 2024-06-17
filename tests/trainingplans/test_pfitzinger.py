from tests.trainingplans.base_test import BaseTest
from trainingplans.lists import PfitzingerLists


class TrainingPlanTestCase(BaseTest):
    def test_trainingplan_pfitzinger(self) -> None:
        self.check_workout_files(PfitzingerLists)
