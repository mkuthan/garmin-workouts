import unittest

import account
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.fields import get_step_type, get_sport_type, get_end_condition
from garminworkouts.models.fields import get_intensity_type, get_target_type, get_equipment_type, get_stroke_type
from garminworkouts.models.fields import _STEP_TYPE, _SPORT_TYPE, _STROKE_TYPE, _CONDITION_TYPE
from garminworkouts.models.fields import _INTENSITY_TYPE, _WORKOUT_TARGET, _EQUIPMENT_TYPE


def _garmin_client():
    return GarminClient(
        connect_url="https://connect.garmin.com",
        sso_url="https://sso.garmin.com",
        username=account.USERNAME,
        password=account.PASSWORD,
        cookie_jar=".garmin-cookies.txt")


class TypesTestCase(unittest.TestCase):
    def test_types(self):
        with _garmin_client() as connection:
            types = connection.list_types()

            for type in types.keys():
                for i in range(len(types[type])-1):
                    with self.subTest(type):
                        elem = types[type][i]
                        if type == "workoutStepTypes":
                            self.assertEqual(elem[f"{_STEP_TYPE}Id"],
                                             get_step_type(elem[f"{_STEP_TYPE}Key"])[
                                                 f"{_STEP_TYPE}Id"])
                        elif type == "workoutSportTypes":
                            self.assertEqual(elem[f"{_SPORT_TYPE}Id"],
                                             get_sport_type(elem[f"{_SPORT_TYPE}Key"])[
                                                 f"{_SPORT_TYPE}Id"])
                        elif type == "workoutConditionTypes":
                            self.assertEqual(elem[f"{_CONDITION_TYPE}Id"],
                                             get_end_condition(elem[f"{_CONDITION_TYPE}Key"])[
                                                 f"{_CONDITION_TYPE}Id"])
                        elif type == "workoutIntensityTypes":
                            self.assertEqual(elem[f"{_INTENSITY_TYPE}Id"],
                                             get_intensity_type(elem[f"{_INTENSITY_TYPE}Key"])[
                                                 f"{_INTENSITY_TYPE}Id"])
                        elif type == "workoutTargetTypes":
                            self.assertEqual(elem[f"{_WORKOUT_TARGET}Id"],
                                             get_target_type(elem[f"{_WORKOUT_TARGET}Key"])[
                                                 f"{_WORKOUT_TARGET}Id"])
                        elif type == "workoutEquipmentTypes":
                            self.assertEqual(elem[f"{_EQUIPMENT_TYPE}Id"],
                                             get_equipment_type(elem[f"{_EQUIPMENT_TYPE}Key"])[
                                                 f"{_EQUIPMENT_TYPE}Id"])
                        elif type == "workoutStrokeTypes":
                            self.assertEqual(elem[f"{_STROKE_TYPE}Id"],
                                             get_stroke_type(elem[f"{_STROKE_TYPE}Key"])[
                                                 f"{_STROKE_TYPE}Id"])


if __name__ == "__main__":
    unittest.main()
