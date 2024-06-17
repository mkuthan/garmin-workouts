from tests.trainingplans.base_test import BaseTest
from trainingplans.lists import (TriathlonOlympic, TriathlonSprint)


class TrainingPlanTestCase(BaseTest):
    def test_trainingplan_garmin_triathlonolympic(self) -> None:
        self.check_workout_files(TriathlonOlympic)

    def test_trainingplan_garmin_triathlonsprint(self) -> None:
        self.check_workout_files(TriathlonSprint)
