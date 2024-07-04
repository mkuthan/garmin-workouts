import unittest
from garminworkouts.models.fields import (SPORT_TYPES, INTENSITY_TYPES, STEP_TYPES, CONDITION_TYPES, TARGET_TYPES,
                                          EVENT_TYPES,
                                          ACTIVITY_TYPES,
                                          UNIT_TYPES,
                                          DRILL_TYPES,
                                          EQUIPMENT_TYPES, STROKE_TYPES, SWIMINSTRUCTION_TYPES, _SPORT_TYPE_KEY,
                                          _SPORT_TYPE_ID, _INTENSITY_TYPE_KEY, _INTENSITY_TYPE_ID, _TARGET, _ZONE,
                                          _SECONDARY_TARGET, _SECONDARY_ZONE, _STEP_TYPE_ID, _STEP_TYPE_KEY,
                                          _CONDITION_TYPE_ID,
                                          _CONDITION_TYPE_KEY,
                                          _WORKOUT_TARGET_ID, _WORKOUT_TARGET_KEY, _STROKE_TYPE_ID, _STROKE_TYPE_KEY,
                                          _EQUIPMENT_TYPE_ID, _EQUIPMENT_TYPE_KEY, _WEIGHT_VALUE, _WEIGHT_UNIT,
                                          _UNIT_ID, _UNIT_KEY, _FACTOR, _SWIM_INSTRUCTION_TYPE_ID,
                                          _SWIM_INSTRUCTION_TYPE_KEY, _DRILL_TYPE_ID, _DRILL_TYPE_KEY,
                                          _ACTIVITY_TYPE_ID, _ACTIVITY_TYPE_KEY, _EVENT_TYPE_ID, _EVENT_TYPE_KEY)
from garminworkouts.models.fields import (get_sport_type, get_intensity_type,
                                          get_target_fields, get_step_type, get_end_condition, get_target_type,
                                          get_stroke_type, get_equipment_type, get_weight, get_unit_type, get_estimate,
                                          get_pool, get_swim_instruction_type, get_drill_type, get_activity_type,
                                          get_event_type)


class FieldsTestCase(unittest.TestCase):
    def test_get_sport_type(self) -> None:
        for type, index in SPORT_TYPES.items():
            self.assertEqual(get_sport_type(type), {
                             _SPORT_TYPE_ID: index, _SPORT_TYPE_KEY: type})
        self.assertEqual(get_sport_type('invalid'), {})

    def test_get_intensity_type(self) -> None:
        for type, index in INTENSITY_TYPES.items():
            self.assertEqual(get_intensity_type(type), {_INTENSITY_TYPE_ID: index, _INTENSITY_TYPE_KEY: type})
        self.assertEqual(get_intensity_type('invalid'), {})

    def test_get_target_fields(self) -> None:
        self.assertEqual(get_target_fields(False), (_TARGET, _ZONE))
        self.assertEqual(get_target_fields(True), (_SECONDARY_TARGET, _SECONDARY_ZONE))

    def test_get_step_type(self) -> None:
        for type, index in STEP_TYPES.items():
            self.assertEqual(get_step_type(type), {_STEP_TYPE_ID: index, _STEP_TYPE_KEY: type})
        self.assertEqual(get_step_type('invalid'), {})

    def test_get_end_condition(self) -> None:
        for type, index in CONDITION_TYPES.items():
            self.assertEqual(get_end_condition(type), {_CONDITION_TYPE_ID: index, _CONDITION_TYPE_KEY: type})
        self.assertEqual(get_end_condition('invalid'), {})

    def test_get_target_type(self) -> None:
        for type, index in TARGET_TYPES.items():
            self.assertEqual(get_target_type(type), {_WORKOUT_TARGET_ID: index, _WORKOUT_TARGET_KEY: type})
        self.assertEqual(get_target_type('invalid'), {})

    def test_get_equipment_type(self) -> None:
        for type, index in EQUIPMENT_TYPES.items():
            self.assertEqual(get_equipment_type(type), {
                             _EQUIPMENT_TYPE_ID: index, _EQUIPMENT_TYPE_KEY: type})
        self.assertEqual(get_equipment_type('invalid'), {})

    def test_get_stroke_type(self) -> None:
        for type, index in STROKE_TYPES.items():
            self.assertEqual(get_stroke_type(type), {
                             _STROKE_TYPE_ID: index, _STROKE_TYPE_KEY: type})
        self.assertEqual(get_stroke_type('invalid'), {})

    def test_get_swim_instruction_type(self) -> None:
        for type, index in SWIMINSTRUCTION_TYPES.items():
            self.assertEqual(get_swim_instruction_type(type), {
                             _SWIM_INSTRUCTION_TYPE_ID: index, _SWIM_INSTRUCTION_TYPE_KEY: type})
        self.assertEqual(get_stroke_type('invalid'), {})

    def test_get_drill_type(self) -> None:
        for type, index in DRILL_TYPES.items():
            self.assertEqual(get_drill_type(type), {
                             _DRILL_TYPE_ID: index, _DRILL_TYPE_KEY: type})
        self.assertEqual(get_drill_type('invalid'), {})

    def test_get_unit_type(self) -> None:
        for type, index in UNIT_TYPES.items():
            self.assertEqual(get_unit_type(type), {_UNIT_ID: index[0], _UNIT_KEY: type, _FACTOR: index[1]})
        self.assertEqual(get_unit_type('invalid'), {})

    def test_get_activity_type(self) -> None:
        for type, index in ACTIVITY_TYPES.items():
            self.assertEqual(get_activity_type(type), {
                             _ACTIVITY_TYPE_ID: index, _ACTIVITY_TYPE_KEY: type})
        self.assertEqual(get_activity_type('invalid'), {})

    def test_get_event_type(self) -> None:
        for type, index in EVENT_TYPES.items():
            self.assertEqual(get_event_type(type), {
                             _EVENT_TYPE_ID: index, _EVENT_TYPE_KEY: type})
        self.assertEqual(get_event_type('invalid'), {})

    def test_get_weight(self) -> None:
        self.assertEqual(get_weight(50, 'kilogram'), {_WEIGHT_VALUE: 50,
                         _WEIGHT_UNIT: {_UNIT_ID: 8, _UNIT_KEY: 'kilogram', _FACTOR: 1000}})
        self.assertEqual(get_weight(150, 'pound'), {_WEIGHT_VALUE: 150, _WEIGHT_UNIT: {
                         _UNIT_ID: 9, _UNIT_KEY: 'pound', _FACTOR: 453.59237}})
        self.assertEqual(get_weight(None, 'kg'), {})

    def test_get_estimate(self) -> None:
        self.assertEqual(get_estimate('DISTANCE_ESTIMATED'), {
            'estimateType': 'DISTANCE_ESTIMATED',
            'estimatedDistanceUnit': {
                         _UNIT_ID: 2, _UNIT_KEY: 'kilometer', _FACTOR: 100000.0}})
        self.assertEqual(get_estimate(None), {})

    def test_get_pool(self) -> None:
        self.assertEqual(get_pool('25m'), {'poolLength': 25, 'poolLengthUnit': {
                         _UNIT_ID: 1, _UNIT_KEY: 'meter', _FACTOR: 100.0}})
        self.assertEqual(get_pool('50m'), {'poolLength': 50, 'poolLengthUnit': {
                         _UNIT_ID: 1, _UNIT_KEY: 'meter', _FACTOR: 100.0}})
        self.assertEqual(get_pool(None), {})


if __name__ == '__main__':
    unittest.main()
