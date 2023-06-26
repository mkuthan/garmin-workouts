import unittest

import account
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.fields import get_step_type, get_sport_type, get_end_condition
from garminworkouts.models.fields import get_intensity_type, get_target_type, get_equipment_type, get_stroke_type
from garminworkouts.models.fields import _STEP_TYPE_FIELD, _SPORT_TYPE_FIELD, _STROKE_TYPE_FIELD, _CONDITION_TYPE_FIELD
from garminworkouts.models.fields import _INTENSITY_TYPE_FIELD, _WORKOUT_TARGET_FIELD, _EQUIPMENT_TYPE_FIELD


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
                            self.assertEqual(elem[f"{_STEP_TYPE_FIELD}Id"],
                                             get_step_type(elem[f"{_STEP_TYPE_FIELD}Key"])[
                                                 f"{_STEP_TYPE_FIELD}Id"])
                        elif type == "workoutSportTypes":
                            self.assertEqual(elem[f"{_SPORT_TYPE_FIELD}Id"],
                                             get_sport_type(elem[f"{_SPORT_TYPE_FIELD}Key"])[
                                                 f"{_SPORT_TYPE_FIELD}Id"])
                        elif type == "workoutConditionTypes":
                            self.assertEqual(elem[f"{_CONDITION_TYPE_FIELD}Id"],
                                             get_end_condition(elem[f"{_CONDITION_TYPE_FIELD}Key"])[
                                                 f"{_CONDITION_TYPE_FIELD}Id"])
                        elif type == "workoutIntensityTypes":
                            self.assertEqual(elem[f"{_INTENSITY_TYPE_FIELD}Id"],
                                             get_intensity_type(elem[f"{_INTENSITY_TYPE_FIELD}Key"])[
                                                 f"{_INTENSITY_TYPE_FIELD}Id"])
                        elif type == "workoutTargetTypes":
                            self.assertEqual(elem[f"{_WORKOUT_TARGET_FIELD}Id"],
                                             get_target_type(elem[f"{_WORKOUT_TARGET_FIELD}Key"])[
                                                 f"{_WORKOUT_TARGET_FIELD}Id"])
                        elif type == "workoutEquipmentTypes":
                            self.assertEqual(elem[f"{_EQUIPMENT_TYPE_FIELD}Id"],
                                             get_equipment_type(elem[f"{_EQUIPMENT_TYPE_FIELD}Key"])[
                                                 f"{_EQUIPMENT_TYPE_FIELD}Id"])
                        elif type == "workoutStrokeTypes":
                            self.assertEqual(elem[f"{_STROKE_TYPE_FIELD}Id"],
                                             get_stroke_type(elem[f"{_STROKE_TYPE_FIELD}Key"])[
                                                 f"{_STROKE_TYPE_FIELD}Id"])


if __name__ == "__main__":
    unittest.main()
