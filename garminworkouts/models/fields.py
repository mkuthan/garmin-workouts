from typing import Any
from garminworkouts.models.types import (EVENT_TYPES, SPORT_TYPES, INTENSITY_TYPES, STEP_TYPES, UNIT_TYPES,
                                         CONDITION_TYPES, TARGET_TYPES, STROKE_TYPES, EQUIPMENT_TYPES,
                                         SWIMINSTRUCTION_TYPES, DRILL_TYPES, ACTIVITY_TYPES)

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
_SWIM_INSTRUCTION = 'swimInstruction'
_DRILL = 'drill'
_ACTIVITY = 'activity'
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
_AUTHOR = 'author'


def create_field_name(prefix, suffix) -> str:
    return f'{prefix}{suffix.capitalize()}'


def create_field_value(key: str, value: Any, name: str) -> dict:
    return {
        f'{key}Id': value,
        f'{key}Key': name,
    } if value else {}


_SUBSPORT: str = create_field_name('sub', _SPORT)
_WORKOUT_ID: str = create_field_name(_WORKOUT, _ID)
_WORKOUT_NAME: str = create_field_name(_WORKOUT, _NAME)
_WORKOUT_OWNER_ID: str = create_field_name(_OWNER, _ID)
_WORKOUT_SPORT_TYPE: str = create_field_name(_SPORT, _TYPE)
_WORKOUT_SUBSPORT_TYPE: str = create_field_name(_SUBSPORT, _TYPE)
_WORKOUT_SEGMENTS: str = create_field_name(_WORKOUT, _SEGMENT + 's')
_WORKOUT_STEPS: str = create_field_name(_WORKOUT, _STEP + 's')
_WORKOUT_ORDER: str = create_field_name(_SEGMENT, _ORDER)
_SPORT_TYPE: str = create_field_name(_SPORT, _TYPE)
_INTENSITY_TYPE: str = create_field_name(_INTENSITY, _TYPE)
_STEP_TYPE: str = create_field_name(_STEP, _TYPE)
_CONDITION_TYPE: str = create_field_name(_CONDITION, _TYPE)
_STROKE_TYPE: str = create_field_name(_STROKE, _TYPE)
_EQUIPMENT_TYPE: str = create_field_name(_EQUIPMENT, _TYPE)
_SWIM_INSTRUCTION_TYPE: str = create_field_name(_SWIM_INSTRUCTION, _TYPE)
_DRILL_TYPE: str = create_field_name(_DRILL, _TYPE)
_ACTIVITY_TYPE: str = _TYPE
_EVENT_TYPE: str = _TYPE
_END_CONDITION: str = create_field_name('end', _CONDITION)
_WORKOUT_TARGET: str = create_field_name(create_field_name(_WORKOUT, _TARGET), _TYPE)

_EVENT_NAME: str = create_field_name(_EVENT, _NAME)
_EVENT_TIME: str = create_field_name(_EVENT, _TIME + _LOCAL)
_COURSE_ID: str = create_field_name(_COURSE, _ID)

_SPORT_TYPE_ID: str = create_field_name(_SPORT_TYPE, _ID)
_SPORT_TYPE_KEY: str = create_field_name(_SPORT_TYPE, _KEY)
_INTENSITY_TYPE_ID: str = create_field_name(_INTENSITY_TYPE, _ID)
_INTENSITY_TYPE_KEY: str = create_field_name(_INTENSITY_TYPE, _KEY)
_STEP_TYPE_ID: str = create_field_name(_STEP_TYPE, _ID)
_STEP_TYPE_KEY: str = create_field_name(_STEP_TYPE, _KEY)
_CONDITION_TYPE_ID: str = create_field_name(_CONDITION_TYPE, _ID)
_CONDITION_TYPE_KEY: str = create_field_name(_CONDITION_TYPE, _KEY)
_WORKOUT_TARGET_ID: str = create_field_name(_WORKOUT_TARGET, _ID)
_WORKOUT_TARGET_KEY: str = create_field_name(_WORKOUT_TARGET, _KEY)
_STROKE_TYPE_ID: str = create_field_name(_STROKE_TYPE, _ID)
_STROKE_TYPE_KEY: str = create_field_name(_STROKE_TYPE, _KEY)
_EQUIPMENT_TYPE_ID: str = create_field_name(_EQUIPMENT_TYPE, _ID)
_EQUIPMENT_TYPE_KEY: str = create_field_name(_EQUIPMENT_TYPE, _KEY)
_SECONDARY_TARGET: str = create_field_name(_SECONDARY, _TARGET)
_SECONDARY_ZONE: str = create_field_name(_SECONDARY, _ZONE)
_WEIGHT_VALUE: str = create_field_name(_WEIGHT, _VALUE)
_WEIGHT_UNIT: str = create_field_name(_WEIGHT, _UNIT)
_UNIT_ID: str = create_field_name(_UNIT, _ID)
_UNIT_KEY: str = create_field_name(_UNIT, _KEY)
_SWIM_INSTRUCTION_TYPE_ID: str = create_field_name(_SWIM_INSTRUCTION_TYPE, _ID)
_SWIM_INSTRUCTION_TYPE_KEY: str = create_field_name(_SWIM_INSTRUCTION_TYPE, _KEY)
_DRILL_TYPE_ID: str = create_field_name(_DRILL_TYPE, _ID)
_DRILL_TYPE_KEY: str = create_field_name(_DRILL_TYPE, _KEY)
_ACTIVITY_TYPE_ID: str = create_field_name(_ACTIVITY_TYPE, _ID)
_ACTIVITY_TYPE_KEY: str = create_field_name(_ACTIVITY_TYPE, _KEY)
_EVENT_TYPE_ID: str = create_field_name(_EVENT_TYPE, _ID)
_EVENT_TYPE_KEY: str = create_field_name(_EVENT_TYPE, _KEY)
_STEP_ORDER: str = create_field_name(_STEP, _ORDER)
_EXERCISE_NAME: str = create_field_name(_EXERCISE, _NAME)
_STEPS: str = _STEP + 's'
_CHILD_STEP_ID: str = create_field_name(create_field_name('child', _STEP), _ID)
_ITERATIONS = 'numberOfIterations'
_REPEAT = 'smartRepeat'
_REPEAT_DURATION = 'repeatDuration'
_COMPARE = 'compare'
_STEP_ID: str = create_field_name(_STEP, _ID)
_END_CONDITION_VALUE: str = create_field_name(_END_CONDITION, _VALUE)
_END_CONDITION_COMPARE: str = create_field_name(_END_CONDITION, _COMPARE)
_END_CONDITION_ZONE: str = create_field_name(_END_CONDITION, _ZONE)
_REPEAT_GROUP = 'RepeatGroupDTO'
_EXECUTABLE_STEP = 'ExecutableStepDTO'
_PREFERRED_END_CONDITION_UNIT: str = create_field_name(create_field_name('preferredEnd', _CONDITION), _UNIT)

_ESTIMATED_DURATION = 'estimatedDurationInSecs'
_ESTIMATED_DISTANCE = 'estimatedDistanceInMeters'
_AVG_SPEED = 'avgTrainingSpeed'


def get_sport_type(sport_type) -> dict:
    return create_field_value(create_field_name(_SPORT, _TYPE), SPORT_TYPES.get(sport_type, ''), str(sport_type))


def get_intensity_type(target_type) -> dict:
    return create_field_value(create_field_name(_INTENSITY, _TYPE), INTENSITY_TYPES.get(target_type), target_type)


def get_target_fields(secondary) -> tuple[str, str]:
    target: str = create_field_name(_TARGET, '') if not secondary else create_field_name(_SECONDARY, _TARGET)
    zone: str = create_field_name(_ZONE, '') if not secondary else create_field_name(_SECONDARY, _ZONE)
    return target, zone


def get_step_type(step_type) -> dict:
    return create_field_value(create_field_name(_STEP, _TYPE), STEP_TYPES.get(step_type), step_type)


def get_end_condition(end_condition) -> dict:
    return create_field_value(create_field_name(_CONDITION, _TYPE), CONDITION_TYPES.get(end_condition), end_condition)


def get_target_type(target_type) -> dict:
    return create_field_value(create_field_name(create_field_name(_WORKOUT, _TARGET), _TYPE),
                              TARGET_TYPES.get(target_type), target_type)


def get_stroke_type(stroke_type) -> dict:
    return create_field_value(create_field_name(_STROKE, _TYPE), STROKE_TYPES.get(stroke_type), stroke_type)


def get_equipment_type(equipment_type) -> dict:
    return create_field_value(create_field_name(_EQUIPMENT, _TYPE), EQUIPMENT_TYPES.get(equipment_type), equipment_type)


def get_weight(weight, unit) -> dict:
    return {
        _WEIGHT_VALUE: weight,
        _WEIGHT_UNIT: get_unit_type(unit)
    } if weight else {}


def get_unit_type(unit) -> dict:
    return {
        _UNIT_ID: UNIT_TYPES[unit][0],
        _UNIT_KEY: unit,
        _FACTOR: UNIT_TYPES[unit][1],
    } if unit in UNIT_TYPES else {}


@staticmethod
def get_estimate(type) -> dict[str, dict]:
    unit = 'kilometer'
    return {
        'estimateType': type,
        'estimatedDistanceUnit': get_unit_type(unit)
    } if type else {}


def get_pool(pool) -> dict:
    if pool == '25m':
        length = 25
        unit = 'meter'
    elif pool == '50m':
        length = 50
        unit = 'meter'
    else:
        length = 25
        unit = 'meter'

    return {
        'poolLength': length,
        'poolLengthUnit': get_unit_type(unit)
    } if pool else {}


def get_swim_instruction_type(instruction) -> dict:
    return create_field_value(create_field_name(_SWIM_INSTRUCTION, _TYPE), SWIMINSTRUCTION_TYPES.get(instruction),
                              instruction)


def get_drill_type(drill) -> dict:
    return create_field_value(create_field_name(_DRILL, _TYPE), DRILL_TYPES.get(drill), drill)


def get_activity_type(activity) -> dict:
    return create_field_value(_ACTIVITY_TYPE, ACTIVITY_TYPES.get(activity), activity)


def get_event_type(event) -> dict:
    return create_field_value(_EVENT_TYPE, EVENT_TYPES.get(event), event)
