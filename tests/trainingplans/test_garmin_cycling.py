from tests.trainingplans.base_test import BaseTest
from trainingplans.lists import (CyclingCentury, CyclingGranFondo, CyclingRace, CyclingMetricCentury, CyclingMTB)


class TrainingPlanTestCase(BaseTest):
    def test_trainingplan_garmin_cycling_crit(self) -> None:
        self.check_workout_files(CyclingRace)

    def test_trainingplan_garmin_cycling_fullcentury(self) -> None:
        self.check_workout_files(CyclingCentury)

    def test_trainingplan_garmin_cycling_granfondo(self) -> None:
        self.check_workout_files(CyclingGranFondo)

    def test_trainingplan_garmin_cycling_halfcentury(self) -> None:
        self.check_workout_files(CyclingMetricCentury)

    def test_trainingplan_garmin_cycling_MTB(self) -> None:
        self.check_workout_files(CyclingMTB)
