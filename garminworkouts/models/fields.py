from garminworkouts.models.types import SPORT_TYPES, INTENSITY_TYPES, STEP_TYPES
from garminworkouts.models.types import END_CONDITIONS, TARGET_TYPES, STROKE_TYPES, EQUIPMENT_TYPES

_WORKOUT = 'workout'
_SPORT = 'sport'
_DESCRIPTION = 'description'
_TARGET = 'target'
_TYPE = 'type'
_STEP = 'step'
_SEGMENT = 'segment'
_DURATION = 'duration'
_WEIGHT = 'weight'
_UNIT = 'unit'
_GOAL = 'goal'
_DISTANCE = 'distance'
_ID = 'id'
_NAME = 'name'
_OWNER = 'owner'
_ORDER = 'order'
_CATEGORY = 'category'
_INTENSITY = 'intensity'
_EQUIPMENT = 'equipment'
_CONDITION = 'condition'
_STROKE = 'stroke'
_COURSE = 'course'
_EVENT = 'event'
_DATE = 'date'
_LOCATION = 'location'
_KEY = 'key'
_VALUE = 'value'
_UNIT = 'unit'
_FACTOR = 'factor'
_ZONE = 'zone'
_SECONDARY = 'secondary'
_TIME = 'time'
_LOCAL = 'local'
_EXERCISE = 'exercise'


_WORKOUT_ID = f'{_WORKOUT}{_ID.capitalize()}'
_WORKOUT_NAME = f'{_WORKOUT}{_NAME.capitalize()}'
_WORKOUT_OWNER_ID = f'{_OWNER}{_ID.capitalize()}'
_WORKOUT_SPORT_TYPE = f'{_SPORT}{_TYPE.capitalize()}'
_WORKOUT_SEGMENTS = f'{_WORKOUT}{_SEGMENT.capitalize()}s'
_WORKOUT_STEPS = f'{_WORKOUT}{_STEP.capitalize()}s'
_WORKOUT_ORDER = f'{_SEGMENT}{_ORDER.capitalize()}'
_SPORT_TYPE = f'{_SPORT}{_TYPE.capitalize()}'
_INTENSITY_TYPE = f'{_INTENSITY}{_TYPE.capitalize()}'
_STEP_TYPE = f'{_STEP}{_TYPE.capitalize()}'
_CONDITION_TYPE = f'{_CONDITION}{_TYPE.capitalize()}'
_STROKE_TYPE = f'{_STROKE}{_TYPE.capitalize()}'
_EQUIPMENT_TYPE = f'{_EQUIPMENT}{_TYPE.capitalize()}'
_END_CONDITION = f'end{_CONDITION.capitalize()}'
_WORKOUT_TARGET = f'{_WORKOUT}{_TARGET.capitalize()}{_TYPE.capitalize()}'

_EVENT_NAME = f'{_EVENT}{_NAME.capitalize()}'
_EVENT_TIME = f'{_EVENT}{_TIME.capitalize()}{_LOCAL.capitalize()}'
_COURSE_ID = f'{_COURSE}{_ID.capitalize()}'

_SPORT_TYPE_ID = f'{_SPORT_TYPE}{_ID.capitalize()}'
_SPORT_TYPE_KEY = f'{_SPORT_TYPE}{_KEY.capitalize()}'
_INTENSITY_TYPE_ID = f'{_INTENSITY_TYPE}{_ID.capitalize()}'
_INTENSITY_TYPE_KEY = f'{_INTENSITY_TYPE}{_KEY.capitalize()}'
_STEP_TYPE_ID = f'{_STEP_TYPE}{_ID.capitalize()}'
_STEP_TYPE_KEY = f'{_STEP_TYPE}{_KEY.capitalize()}'
_CONDITION_TYPE_ID = f'{_CONDITION_TYPE}{_ID.capitalize()}'
_CONDITION_TYPE_KEY = f'{_CONDITION_TYPE}{_KEY.capitalize()}'
_WORKOUT_TARGET_ID = f'{_WORKOUT_TARGET}{_ID.capitalize()}'
_WORKOUT_TARGET_KEY = f'{_WORKOUT_TARGET}{_KEY.capitalize()}'
_STROKE_TYPE_ID = f'{_STROKE_TYPE}{_ID.capitalize()}'
_STROKE_TYPE_KEY = f'{_STROKE_TYPE}{_KEY.capitalize()}'
_EQUIPMENT_TYPE_ID = f'{_EQUIPMENT_TYPE}{_ID.capitalize()}'
_EQUIPMENT_TYPE_KEY = f'{_EQUIPMENT_TYPE}{_KEY.capitalize()}'
_SECONDARY_TARGET = f'{_SECONDARY}{_TARGET.capitalize()}'
_SECONDARY_ZONE = f'{_SECONDARY}{_ZONE.capitalize()}'
_WEIGHT_VALUE = f'{_WEIGHT}{_VALUE.capitalize()}'
_WEIGHT_UNIT = f'{_WEIGHT}{_UNIT.capitalize()}'
_UNIT_ID = f'{_UNIT}{_ID.capitalize()}'
_UNIT_KEY = f'{_UNIT}{_KEY.capitalize()}'
_STEP_ORDER = f'{_STEP}{_ORDER.capitalize()}'
_EXERCISE_NAME = f'{_EXERCISE}{_NAME.capitalize()}'
_STEPS = f'{_STEP}s'
_CHILD_STEP_ID = f'child{_STEP.capitalize()}{_ID.capitalize()}'
_ITERATIONS = 'numberOfIterations'
_REPEAT = 'smartRepeat'
_COMPARE = 'compare'
_STEP_ID = f'{_STEP}{_ID.capitalize()}'
_END_CONDITION_VALUE = f'{_END_CONDITION}{_VALUE.capitalize()}'
_END_CONDITION_COMPARE = f'{_END_CONDITION}{_COMPARE.capitalize()}'
_END_CONDITION_ZONE = f'{_END_CONDITION}{_ZONE.capitalize()}'
_REPEAT_GROUP = 'RepeatGroupDTO'
_EXECUTABLE_STEP = 'ExecutableStepDTO'
_PREFERRED_END_CONDITION_UNIT = f'preferredEnd{_CONDITION.capitalize()}{_UNIT.capitalize()}'


@staticmethod
def get_sport_type(sport_type):
    return {
            _SPORT_TYPE_ID: SPORT_TYPES[sport_type],
            _SPORT_TYPE_KEY: sport_type,
        } if sport_type and sport_type in SPORT_TYPES else {}


@staticmethod
def get_intensity_type(target_type):
    return {
            _INTENSITY_TYPE_ID: INTENSITY_TYPES[target_type],
            _INTENSITY_TYPE_KEY: target_type,
        } if target_type and target_type in INTENSITY_TYPES else {}


@staticmethod
def get_target_fields(secondary):
    target = _TARGET if not secondary else _SECONDARY_TARGET
    zone = _ZONE if not secondary else _SECONDARY_ZONE
    return target, zone


@staticmethod
def get_step_type(step_type):
    return {
        _STEP_TYPE_ID: STEP_TYPES[step_type],
        _STEP_TYPE_KEY: step_type,
    } if step_type and step_type in STEP_TYPES else {}


@staticmethod
def get_end_condition(end_condition):
    return {
        _CONDITION_TYPE_ID: END_CONDITIONS[end_condition],
        _CONDITION_TYPE_KEY: end_condition,
    } if end_condition and end_condition in END_CONDITIONS else {}


@staticmethod
def get_target_type(target_type):
    return {
        _WORKOUT_TARGET_ID: TARGET_TYPES[target_type],
        _WORKOUT_TARGET_KEY: target_type,
    } if target_type and target_type in TARGET_TYPES else {}


@staticmethod
def get_stroke_type(stroke_type):
    return {
        _STROKE_TYPE_ID: STROKE_TYPES[stroke_type],
        _STROKE_TYPE_KEY: stroke_type,
    } if stroke_type and stroke_type in STROKE_TYPES else {}


@staticmethod
def get_equipment_type(equipment_type):
    return {
        _EQUIPMENT_TYPE_ID: EQUIPMENT_TYPES[equipment_type],
        _EQUIPMENT_TYPE_KEY: equipment_type,
    } if equipment_type and equipment_type in EQUIPMENT_TYPES else {}


@staticmethod
def get_weight(weight):
    return {
        _WEIGHT_VALUE: weight,
        _WEIGHT_UNIT: {
            _UNIT_ID: 8,
            _UNIT_KEY: 'kilogram',
            _FACTOR: 1000.0
        }
    } if weight else {}
