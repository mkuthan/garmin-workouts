from garminworkouts.models.types import SPORT_TYPES, INTENSITY_TYPES, STEP_TYPES
from garminworkouts.models.types import END_CONDITIONS, TARGET_TYPES, STROKE_TYPES, EQUIPMENT_TYPES

_WORKOUT_ID_FIELD = "workoutId"
_WORKOUT_NAME_FIELD = "workoutName"
_WORKOUT_DESCRIPTION_FIELD = "description"
_WORKOUT_OWNER_ID_FIELD = "ownerId"
_WORKOUT_SPORT_TYPE_FIELD = "sportType"
_WORKOUT_SEGMENTS_FIELD = "workoutSegments"
_WORKOUT_STEPS_FIELD = "workoutSteps"
_WORKOUT_ORDER_FIELD = "segmentOrder"
_SPORT_TYPE_FIELD = "sportType"
_INTENSITY_TYPE_FIELD = "intensityType"
_STEP_TYPE_FIELD = "stepType"
_CONDITION_TYPE_FIELD = "conditionType"
_STROKE_TYPE_FIELD = "strokeType"
_EQUIPMENT_TYPE_FIELD = "equipmentType"
_END_CONDITION_FIELD = "endCondition"
_WORKOUT_TARGET_FIELD = "workoutTargetType"
_WEIGHT_FIELD = "weight"
_UNIT_FIELD = "unit"
_EVENT_ID_FIELD = "id"
_EVENT_NAME_FIELD = "eventName"
_EVENT_DATE_FIELD = "date"
_EVENT_LOCATION_FIELD = "location"
_EVENT_TIME_FIELD = "eventTimeLocal"
_COURSE_FIELD = "courseId"


@staticmethod
def get_sport_type(sport_type):
    return {
            f"{_SPORT_TYPE_FIELD}Id": SPORT_TYPES[sport_type],
            f"{_SPORT_TYPE_FIELD}Key": sport_type,
        } if sport_type and sport_type in SPORT_TYPES else {}


@staticmethod
def get_intensity_type(target_type):
    return {
            f"{_INTENSITY_TYPE_FIELD}Id": INTENSITY_TYPES[target_type],
            f"{_INTENSITY_TYPE_FIELD}Key": target_type,
        } if target_type and target_type in INTENSITY_TYPES else {}


@staticmethod
def get_target_fields(secondary):
    target = 'target' if not secondary else 'secondaryTarget'
    zone = 'zone' if not secondary else 'secondaryZone'
    return target, zone


@staticmethod
def get_step_type(step_type):
    return {
        f"{_STEP_TYPE_FIELD}Id": STEP_TYPES[step_type],
        f"{_STEP_TYPE_FIELD}Key": step_type,
    } if step_type and step_type in STEP_TYPES else {}


@staticmethod
def get_end_condition(end_condition):
    return {
        f"{_CONDITION_TYPE_FIELD}Id": END_CONDITIONS[end_condition],
        f"{_CONDITION_TYPE_FIELD}Key": end_condition,
    } if end_condition and end_condition in END_CONDITIONS else {}


@staticmethod
def get_target_type(target_type):
    return {
        f"{_WORKOUT_TARGET_FIELD}Id": TARGET_TYPES[target_type],
        f"{_WORKOUT_TARGET_FIELD}Key": target_type,
    } if target_type and target_type in TARGET_TYPES else {}


@staticmethod
def get_stroke_type(stroke_type):
    return {
        f"{_STROKE_TYPE_FIELD}Id": STROKE_TYPES[stroke_type],
        f"{_STROKE_TYPE_FIELD}Key": stroke_type,
    } if stroke_type and stroke_type in STROKE_TYPES else {}


@staticmethod
def get_equipment_type(equipment_type):
    return {
        f"{_EQUIPMENT_TYPE_FIELD}Id": EQUIPMENT_TYPES[equipment_type],
        f"{_EQUIPMENT_TYPE_FIELD}Key": equipment_type,
    } if equipment_type and equipment_type in EQUIPMENT_TYPES else {}


@staticmethod
def get_weight(weight):
    return {
        f"{_WEIGHT_FIELD}Value": weight,
        f"{_WEIGHT_FIELD}Unit": {
            f"{_UNIT_FIELD}Id": 8,
            f"{_UNIT_FIELD}Key": "kilogram",
            "factor": 1000.0
        }
    } if weight else {}
