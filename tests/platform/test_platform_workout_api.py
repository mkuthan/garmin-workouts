from tests.trainingplans.base_test import BaseTest
import os


class WorkoutestCase(BaseTest):
    def test_workout(self) -> None:
        workout_files: list = [
            os.path.join('.', 'trainingplans', 'Running', 'Napier', 'Half', 'Advanced', 'Meso1', '21_1.yaml'),
            os.path.join('.', 'trainingplans', 'Running', '*', '5k', 'Beginner', 'Time', 'R1_1.yaml')
        ]
        self.platform_workout_files(workout_files)
