from tests.trainingplans.base_test import BaseTest
from trainingplans.lists import (Garmin5k, Garmin10k, GarminHalf, GarminMarathon, GarminRunningOther)


class TrainingPlanTestCase(BaseTest):
    def test_trainingplan_garmin_5k(self) -> None:
        self.check_workout_files(Garmin5k)

    def test_trainingplan_garmin_10k(self) -> None:
        self.check_workout_files(Garmin10k)

    def test_trainingplan_garmin_halfmarathon(self) -> None:
        self.check_workout_files(GarminHalf)

    def test_trainingplan_garmin_marathon(self) -> None:
        self.check_workout_files(GarminMarathon)

    def test_trainingplan_garmin_runningother(self) -> None:
        self.check_workout_files(GarminRunningOther)
