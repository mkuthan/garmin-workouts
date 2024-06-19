from garminworkouts.models.types import (EVENT_TYPES, SPORT_TYPES, INTENSITY_TYPES, STEP_TYPES, UNIT_TYPES,
                                         END_CONDITIONS, TARGET_TYPES, STROKE_TYPES, EQUIPMENT_TYPES,
                                         SWIM_INSTRUCTION_TYPES, DRILL_TYPES, ACTIVITY_TYPES)

_WORKOUT = 'workout'
_SPORT = 'sport'
_SUBSPORT = 'subsport'
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


_WORKOUT_ID: str = f'{_WORKOUT}{_ID.capitalize()}'
_WORKOUT_NAME: str = f'{_WORKOUT}{_NAME.capitalize()}'
_WORKOUT_OWNER_ID: str = f'{_OWNER}{_ID.capitalize()}'
_WORKOUT_SPORT_TYPE: str = f'{_SPORT}{_TYPE.capitalize()}'
_WORKOUT_SUBSPORT_TYPE: str = f'sub{_SPORT.capitalize()}{_TYPE.capitalize()}'
_WORKOUT_SEGMENTS: str = f'{_WORKOUT}{_SEGMENT.capitalize()}s'
_WORKOUT_STEPS: str = f'{_WORKOUT}{_STEP.capitalize()}s'
_WORKOUT_ORDER: str = f'{_SEGMENT}{_ORDER.capitalize()}'
_SPORT_TYPE: str = f'{_SPORT}{_TYPE.capitalize()}'
_INTENSITY_TYPE: str = f'{_INTENSITY}{_TYPE.capitalize()}'
_STEP_TYPE: str = f'{_STEP}{_TYPE.capitalize()}'
_CONDITION_TYPE: str = f'{_CONDITION}{_TYPE.capitalize()}'
_STROKE_TYPE: str = f'{_STROKE}{_TYPE.capitalize()}'
_EQUIPMENT_TYPE: str = f'{_EQUIPMENT}{_TYPE.capitalize()}'
_SWIM_INSTRUCTION_TYPE: str = f'{_SWIM_INSTRUCTION}{_TYPE.capitalize()}'
_DRILL_TYPE: str = f'{_DRILL}{_TYPE.capitalize()}'
_ACTIVITY_TYPE: str = _TYPE
_EVENT_TYPE: str = _TYPE
_END_CONDITION: str = f'end{_CONDITION.capitalize()}'
_WORKOUT_TARGET: str = f'{_WORKOUT}{_TARGET.capitalize()}{_TYPE.capitalize()}'

_EVENT_NAME: str = f'{_EVENT}{_NAME.capitalize()}'
_EVENT_TIME: str = f'{_EVENT}{_TIME.capitalize()}{_LOCAL.capitalize()}'
_COURSE_ID: str = f'{_COURSE}{_ID.capitalize()}'

_SPORT_TYPE_ID: str = f'{_SPORT_TYPE}{_ID.capitalize()}'
_SPORT_TYPE_KEY: str = f'{_SPORT_TYPE}{_KEY.capitalize()}'
_INTENSITY_TYPE_ID: str = f'{_INTENSITY_TYPE}{_ID.capitalize()}'
_INTENSITY_TYPE_KEY: str = f'{_INTENSITY_TYPE}{_KEY.capitalize()}'
_STEP_TYPE_ID: str = f'{_STEP_TYPE}{_ID.capitalize()}'
_STEP_TYPE_KEY: str = f'{_STEP_TYPE}{_KEY.capitalize()}'
_CONDITION_TYPE_ID: str = f'{_CONDITION_TYPE}{_ID.capitalize()}'
_CONDITION_TYPE_KEY: str = f'{_CONDITION_TYPE}{_KEY.capitalize()}'
_WORKOUT_TARGET_ID: str = f'{_WORKOUT_TARGET}{_ID.capitalize()}'
_WORKOUT_TARGET_KEY: str = f'{_WORKOUT_TARGET}{_KEY.capitalize()}'
_STROKE_TYPE_ID: str = f'{_STROKE_TYPE}{_ID.capitalize()}'
_STROKE_TYPE_KEY: str = f'{_STROKE_TYPE}{_KEY.capitalize()}'
_EQUIPMENT_TYPE_ID: str = f'{_EQUIPMENT_TYPE}{_ID.capitalize()}'
_EQUIPMENT_TYPE_KEY: str = f'{_EQUIPMENT_TYPE}{_KEY.capitalize()}'
_SECONDARY_TARGET: str = f'{_SECONDARY}{_TARGET.capitalize()}'
_SECONDARY_ZONE: str = f'{_SECONDARY}{_ZONE.capitalize()}'
_WEIGHT_VALUE: str = f'{_WEIGHT}{_VALUE.capitalize()}'
_WEIGHT_UNIT: str = f'{_WEIGHT}{_UNIT.capitalize()}'
_UNIT_ID: str = f'{_UNIT}{_ID.capitalize()}'
_UNIT_KEY: str = f'{_UNIT}{_KEY.capitalize()}'
_SWIM_INSTRUCTION_TYPE_ID: str = f'{_SWIM_INSTRUCTION_TYPE}{_ID.capitalize()}'
_SWIM_INSTRUCTION_TYPE_KEY: str = f'{_SWIM_INSTRUCTION_TYPE}{_KEY.capitalize()}'
_DRILL_TYPE_ID: str = f'{_DRILL_TYPE}{_ID.capitalize()}'
_DRILL_TYPE_KEY: str = f'{_DRILL_TYPE}{_KEY.capitalize()}'
_ACTIVITY_TYPE_ID: str = f'{_ACTIVITY_TYPE}{_ID.capitalize()}'
_ACTIVITY_TYPE_KEY: str = f'{_ACTIVITY_TYPE}{_KEY.capitalize()}'
_EVENT_TYPE_ID: str = f'{_EVENT_TYPE}{_ID.capitalize()}'
_EVENT_TYPE_KEY: str = f'{_EVENT_TYPE}{_KEY.capitalize()}'
_STEP_ORDER: str = f'{_STEP}{_ORDER.capitalize()}'
_EXERCISE_NAME: str = f'{_EXERCISE}{_NAME.capitalize()}'
_STEPS: str = f'{_STEP}s'
_CHILD_STEP_ID: str = f'child{_STEP.capitalize()}{_ID.capitalize()}'
_ITERATIONS = 'numberOfIterations'
_REPEAT = 'smartRepeat'
_REPEAT_DURATION = 'repeatDuration'
_COMPARE = 'compare'
_STEP_ID: str = f'{_STEP}{_ID.capitalize()}'
_END_CONDITION_VALUE: str = f'{_END_CONDITION}{_VALUE.capitalize()}'
_END_CONDITION_COMPARE: str = f'{_END_CONDITION}{_COMPARE.capitalize()}'
_END_CONDITION_ZONE: str = f'{_END_CONDITION}{_ZONE.capitalize()}'
_REPEAT_GROUP = 'RepeatGroupDTO'
_EXECUTABLE_STEP = 'ExecutableStepDTO'
_PREFERRED_END_CONDITION_UNIT: str = f'preferredEnd{_CONDITION.capitalize()}{_UNIT.capitalize()}'

_ESTIMATED_DURATION = 'estimatedDurationInSecs'
_ESTIMATED_DISTANCE = 'estimatedDistanceInMeters'
_AVG_SPEED = 'avgTrainingSpeed'


@staticmethod
def get_sport_type(sport_type) -> dict:
    return {
            _SPORT_TYPE_ID: SPORT_TYPES.get(sport_type),
            _SPORT_TYPE_KEY: sport_type,
        } if sport_type and sport_type in SPORT_TYPES else {}


@staticmethod
def get_intensity_type(target_type) -> dict:
    return {
            _INTENSITY_TYPE_ID: INTENSITY_TYPES.get(target_type),
            _INTENSITY_TYPE_KEY: target_type,
        } if target_type and target_type in INTENSITY_TYPES else {}


@staticmethod
def get_target_fields(secondary) -> tuple[str, str]:
    target: str = _TARGET if not secondary else _SECONDARY_TARGET
    zone: str = _ZONE if not secondary else _SECONDARY_ZONE
    return target, zone


@staticmethod
def get_step_type(step_type) -> dict:
    return {
        _STEP_TYPE_ID: STEP_TYPES.get(step_type),
        _STEP_TYPE_KEY: step_type,
    } if step_type and step_type in STEP_TYPES else {}


@staticmethod
def get_end_condition(end_condition) -> dict:
    return {
        _CONDITION_TYPE_ID: END_CONDITIONS.get(end_condition),
        _CONDITION_TYPE_KEY: end_condition,
    } if end_condition and end_condition in END_CONDITIONS else {}


@staticmethod
def get_target_type(target_type) -> dict:
    return {
        _WORKOUT_TARGET_ID: TARGET_TYPES.get(target_type),
        _WORKOUT_TARGET_KEY: target_type,
    } if target_type and target_type in TARGET_TYPES else {}


@staticmethod
def get_stroke_type(stroke_type) -> dict:
    return {
        _STROKE_TYPE_ID: STROKE_TYPES.get(stroke_type),
        _STROKE_TYPE_KEY: stroke_type,
    } if stroke_type and stroke_type in STROKE_TYPES else {}


@staticmethod
def get_equipment_type(equipment_type) -> dict:
    return {
        _EQUIPMENT_TYPE_ID: EQUIPMENT_TYPES.get(equipment_type),
        _EQUIPMENT_TYPE_KEY: equipment_type,
    } if equipment_type and equipment_type in EQUIPMENT_TYPES else {}


@staticmethod
def get_weight(weight, unit) -> dict:
    return {
        _WEIGHT_VALUE: weight,
        _WEIGHT_UNIT: get_unit_type(unit)
    } if weight else {}


@staticmethod
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


@staticmethod
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
    return {
        _SWIM_INSTRUCTION_TYPE_ID: SWIM_INSTRUCTION_TYPES.get(instruction),
        _SWIM_INSTRUCTION_TYPE_KEY: instruction,
    } if instruction and instruction in SWIM_INSTRUCTION_TYPES else {}


def get_drill_type(drill) -> dict:
    return {
        _DRILL_TYPE_ID: DRILL_TYPES.get(drill),
        _DRILL_TYPE_KEY: drill,
    } if drill and drill in DRILL_TYPES else {}


def get_activity_type(activity) -> dict:
    return {
        _ACTIVITY_TYPE_ID: ACTIVITY_TYPES.get(activity),
        _ACTIVITY_TYPE_KEY: activity,
    } if activity and activity in ACTIVITY_TYPES else {}


def get_event_type(event) -> dict:
    return {
        _EVENT_TYPE_ID: EVENT_TYPES.get(event),
        _EVENT_TYPE_KEY: event,
    } if event and event in EVENT_TYPES else {}
