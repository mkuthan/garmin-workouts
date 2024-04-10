
from garminworkouts.models.duration import Duration
from garminworkouts.models.target import Target

from garminworkouts.models.fields import get_end_condition, _STEP_TYPE, get_step_type, get_stroke_type
from garminworkouts.models.fields import get_equipment_type, _END_CONDITION, get_weight, _TYPE, _CATEGORY
from garminworkouts.models.fields import _STEP_ID, _STEP_ORDER, _CHILD_STEP_ID, _DESCRIPTION, _END_CONDITION_VALUE
from garminworkouts.models.fields import _END_CONDITION_COMPARE, _END_CONDITION_ZONE, _EXERCISE_NAME, _EXECUTABLE_STEP
from garminworkouts.models.fields import _PREFERRED_END_CONDITION_UNIT, _CONDITION_TYPE_KEY, _UNIT_KEY, _DURATION


class WorkoutStep:
    def __init__(
        self,
        order,
        child_step_id,
        description,
        step_type,
        end_condition='lap.button',
        end_condition_value=None,
        target=None,
        secondary_target=None,
        category=None,
        exerciseName=None,
        weight=None,
        equipment=None,
        stroke=None,
    ) -> None:
        '''Valid end condition values:
        - distance: '2.0km', '1.125km', '1.6km'
        - time: 0:40, 4:20
        - lap.button
        '''
        self.order: str = order
        self.child_step_id: str = child_step_id
        self.description: str = description
        self.step_type = step_type
        self.end_condition: str = end_condition
        self.end_condition_value: str | None = end_condition_value
        self.target: Target = target or Target()
        self.secondary_target: Target = secondary_target or Target()
        self.category: tuple = category,
        self.exerciseName = exerciseName,
        self.weight = weight,
        self.equipment: str | None = equipment
        self.stroke: str | None = stroke

    @staticmethod
    def end_condition_unit(end_condition) -> dict | None:
        if end_condition:
            if end_condition.endswith('km'):
                return {_UNIT_KEY: 'kilometer'}
            elif end_condition.endswith('cals'):
                return {_UNIT_KEY: 'calories'}
            else:
                return {_UNIT_KEY: None}
        else:
            return None

    @staticmethod
    def _end_condition(step_config):
        duration = step_config.get(_DURATION)
        if duration:
            if WorkoutStep._str_is_time(duration):
                return get_end_condition('time')
            elif WorkoutStep._str_is_distance(duration):
                return get_end_condition('distance')
            elif WorkoutStep._str_is_calories(duration):
                return get_end_condition('calories')
            elif WorkoutStep._str_is_ppm(duration):
                return get_end_condition('heart.rate')
            elif WorkoutStep._str_is_reps(duration):
                return get_end_condition('reps')
            else:
                return get_end_condition('lap.button')
        return get_end_condition('lap.button')

    @staticmethod
    def _end_condition_key(step_config) -> str:
        return step_config[_CONDITION_TYPE_KEY]

    @staticmethod
    def _end_condition_value(step_config) -> int:
        duration = step_config.get(_DURATION)
        return WorkoutStep.parsed_end_condition_value(duration)

    @staticmethod
    def _str_is_time(string) -> bool:
        return True if ':' in string else False

    @staticmethod
    def _str_to_seconds(time_string) -> int:
        return Duration(str(time_string)).to_seconds()

    @staticmethod
    def _str_is_distance(string) -> bool:
        return True if 'm' in string.lower() else False

    @staticmethod
    def _str_to_meters(string) -> int:
        if 'km' in string.lower():
            return int(float(string.lower().split('km')[0])*1000)
        return int(string.lower().split('m')[0])

    @staticmethod
    def _str_is_calories(string) -> bool:
        return True if 'cals' in string else False

    @staticmethod
    def _str_to_calories(string) -> int:
        return int(string.lower().split('cals')[0])

    @staticmethod
    def _str_is_ppm(string) -> bool:
        return True if 'ppm' in string else False

    @staticmethod
    def _str_to_ppm(string) -> int:
        return int(string.lower().split('ppm')[0])

    @staticmethod
    def _str_is_reps(string) -> bool:
        return True if 'reps' in string else False

    @staticmethod
    def _str_to_reps(string) -> int:
        return int(string.lower().split('reps')[0])

    @staticmethod
    def parsed_end_condition_value(duration) -> int:
        if duration:
            if WorkoutStep._str_is_time(duration):
                return WorkoutStep._str_to_seconds(duration)
            elif WorkoutStep._str_is_distance(duration):
                return WorkoutStep._str_to_meters(duration)
            elif WorkoutStep._str_is_calories(duration):
                return WorkoutStep._str_to_calories(duration)
            elif WorkoutStep._str_is_ppm(duration):
                return WorkoutStep._str_to_ppm(duration)
            elif WorkoutStep._str_is_reps(duration):
                return WorkoutStep._str_to_reps(duration)
            else:
                return int(0)
        else:
            return int(0)

    def create_workout_step(self) -> dict:
        return {
            _TYPE: _EXECUTABLE_STEP,
            _STEP_ID: None,
            _STEP_ORDER: self.order,
            _CHILD_STEP_ID: self.child_step_id,
            _DESCRIPTION: self.description,
            _STEP_TYPE: get_step_type(self.step_type),
            _END_CONDITION: get_end_condition(self.end_condition),
            _PREFERRED_END_CONDITION_UNIT: WorkoutStep.end_condition_unit(self.end_condition),
            _END_CONDITION_VALUE: WorkoutStep.parsed_end_condition_value(self.end_condition_value),
            _END_CONDITION_COMPARE: None,
            _END_CONDITION_ZONE: None,
            _CATEGORY: self.category[0],
            _EXERCISE_NAME: self.exerciseName[0],
            **self.target.create_target(),
            **self.secondary_target.create_target(),
            **get_stroke_type(self.stroke),
            **get_equipment_type(self.equipment),
            **get_weight(self.weight[0], 'kilogram')
        }
