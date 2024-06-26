from tests.trainingplans.base_test import BaseTest
import os


class WorkoutestCase(BaseTest):
    def test_workout(self) -> None:
        workout_file: list = [os.path.join('.', 'trainingplans', 'Running', '*',
                                           'Half', 'Advanced', 'Meso1', '21_1.yaml')]
        self.platform_workout_files(workout_file)
