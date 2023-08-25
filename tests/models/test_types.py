import unittest

import account
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.fields import get_step_type, get_sport_type, get_end_condition
from garminworkouts.models.fields import get_intensity_type, get_target_type, get_equipment_type, get_stroke_type
from garminworkouts.models.fields import _STEP_TYPE_ID, _STEP_TYPE_KEY, _SPORT_TYPE_KEY, _SPORT_TYPE_ID
from garminworkouts.models.fields import _STROKE_TYPE_KEY, _STROKE_TYPE_ID, _CONDITION_TYPE_KEY, _CONDITION_TYPE_ID
from garminworkouts.models.fields import _INTENSITY_TYPE_ID, _INTENSITY_TYPE_KEY, _WORKOUT_TARGET_ID, _WORKOUT_TARGET_KEY,
from garminworkouts.models.fields import _EQUIPMENT_TYPE_ID, _EQUIPMENT_TYPE_KEY


def _garmin_client() -> GarminClient:
    return GarminClient(
        connect_url="https://connect.garmin.com",
        sso_url="https://sso.garmin.com",
        username=account.USERNAME,
        password=account.PASSWORD,
        cookie_jar=".garmin-cookies.txt")


class TypesTestCase(unittest.TestCase):
    def test_types(self) -> None:
        with _garmin_client() as connection:
            types: dict = connection.list_types()

            for type in types.keys():
                for i in range(len(types[type])-1):
                    with self.subTest(type):
                        elem: dict = types[type][i]
                        if type == "workoutStepTypes":
                            self.assertEqual(elem[_STEP_TYPE_ID],
                                             get_step_type(elem[_STEP_TYPE_KEY])[_STEP_TYPE_ID])
                        elif type == "workoutSportTypes":
                            self.assertEqual(elem[_SPORT_TYPE_ID],
                                             get_sport_type(elem[_SPORT_TYPE_KEY])[_SPORT_TYPE_ID])
                        elif type == "workoutConditionTypes":
                            self.assertEqual(elem[_CONDITION_TYPE_ID],
                                             get_end_condition(elem[_CONDITION_TYPE_KEY])[_CONDITION_TYPE_ID])
                        elif type == "workoutIntensityTypes":
                            self.assertEqual(elem[_INTENSITY_TYPE_ID],
                                             get_intensity_type(elem[_INTENSITY_TYPE_KEY])[_INTENSITY_TYPE_ID])
                        elif type == "workoutTargetTypes":
                            self.assertEqual(elem[_WORKOUT_TARGET_ID],
                                             get_target_type(elem[_WORKOUT_TARGET_KEY])[_WORKOUT_TARGET_ID])
                        elif type == "workoutEquipmentTypes":
                            self.assertEqual(elem[_EQUIPMENT_TYPE_ID],
                                             get_equipment_type(elem[_EQUIPMENT_TYPE_KEY])[_EQUIPMENT_TYPE_ID])
                        elif type == "workoutStrokeTypes":
                            self.assertEqual(elem[_STROKE_TYPE_ID],
                                             get_stroke_type(elem[_STROKE_TYPE_KEY])[_STROKE_TYPE_ID])


if __name__ == "__main__":
    unittest.main()
