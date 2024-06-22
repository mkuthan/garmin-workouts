from tests.trainingplans.base_test import BaseTest
from trainingplans.lists import (WorkoutsList, DarebeeLists)


class TrainingPlanTestCase(BaseTest):
    def test_trainingplan_garmin_workouts(self) -> None:
        self.check_workout_files(WorkoutsList)

    def test_trainingplan_darebee(self) -> None:
        self.check_workout_files(DarebeeLists)
