import unittest

from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.workout import Workout

import account


def _garmin_client():
    return GarminClient(
        connect_url="https://connect.garmin.com",
        sso_url="https://sso.garmin.com",
        username=account.USERNAME,
        password=account.PASSWORD,
        cookie_jar=".garmin-cookies.txt")


class WorkoutTestCase(unittest.TestCase):
    def test_types(self):
        with _garmin_client() as connection:
            types = connection.list_types()

            for type in types.keys():
                for i in range(len(types[type])-1):
                    elem = types[type][i]
                    if type == 'workoutStepTypes':
                        self.assertEqual(elem['stepTypeId'],
                                         Workout.get_step_type(elem['stepTypeKey'])['stepTypeId'])
                    elif type == 'workoutSportTypes':
                        self.assertEqual(elem['sportTypeId'],
                                         Workout.get_sport_type(elem['sportTypeKey'])['sportTypeId'])
                    elif type == 'workoutConditionTypes':
                        self.assertEqual(elem['conditionTypeId'],
                                         Workout.get_end_condition(elem['conditionTypeKey'])['conditionTypeId'])
                    elif type == 'workoutIntensityTypes':
                        self.assertEqual(elem['intensityTypeId'],
                                         Workout.get_intensity_type(elem['intensityTypeKey'])['intensityTypeId'])
                    elif type == 'workoutTargetTypes':
                        self.assertEqual(elem['workoutTargetTypeId'],
                                         Workout.get_target_type(elem['workoutTargetTypeKey'])['workoutTargetTypeId'])
                    elif type == 'workoutEquipmentTypes':
                        self.assertEqual(elem['equipmentTypeId'],
                                         Workout.get_equipment_type(elem['equipmentTypeKey'])['equipmentTypeId'])
                    elif type == 'workoutStrokeTypes':
                        self.assertEqual(elem['strokeTypeId'],
                                         Workout.get_stroke_type(elem['strokeTypeKey'])['strokeTypeId'])


if __name__ == '__main__':
    unittest.main()
