
from garminworkouts.models.duration import Duration
from garminworkouts.models.power import Power
from garminworkouts.models.target import Target

from garminworkouts.models.fields import get_end_condition, _STEP_TYPE_FIELD, get_step_type, get_stroke_type
from garminworkouts.models.fields import get_equipment_type, _END_CONDITION_FIELD, get_weight


class WorkoutStep:
    def __init__(
        self,
        order,
        child_step_id,
        description,
        step_type,
        end_condition="lap.button",
        end_condition_value=None,
        target=None,
        secondary_target=None,
        category=None,
        exerciseName=None,
        weight=None,
        equipment=None,
        stroke=None,
    ):
        """Valid end condition values:
        - distance: '2.0km', '1.125km', '1.6km'
        - time: 0:40, 4:20
        - lap.button
        """
        self.order = order
        self.child_step_id = child_step_id
        self.description = description
        self.step_type = step_type
        self.end_condition = end_condition
        self.end_condition_value = end_condition_value
        self.target = target or Target()
        self.secondary_target = secondary_target or Target()
        self.category = category,
        self.exerciseName = exerciseName,
        self.weight = weight,
        self.equipment = equipment
        self.stroke = stroke

    @staticmethod
    def _get_duration(step):
        duration = step.get("duration")
        return Duration(str(duration)) if duration else None

    @staticmethod
    def _get_power(step):
        power = step.get("power")
        return Power(str(power)) if power else None

    @staticmethod
    def end_condition_unit(end_condition):
        if end_condition:
            if end_condition.endswith("km"):
                return {"unitKey": "kilometer"}
            elif end_condition.endswith("cals"):
                return {"unitKey": "calories"}
            else:
                return {"unitKey": None}
        else:
            return None

    @staticmethod
    def _end_condition(step_config):
        duration = step_config.get("duration")
        if duration:
            if WorkoutStep._str_is_time(duration):
                return get_end_condition("time")
            elif WorkoutStep._str_is_distance(duration):
                return get_end_condition("distance")
            elif WorkoutStep._str_is_calories(duration):
                return get_end_condition("calories")
            else:
                return get_end_condition("lap.button")
        return get_end_condition("lap.button")

    @staticmethod
    def _end_condition_key(step_config):
        return step_config['conditionTypeKey']

    @staticmethod
    def _end_condition_value(step_config):
        duration = step_config.get("duration")
        if duration:
            if WorkoutStep._str_is_time(duration):
                return WorkoutStep._str_to_seconds(duration)
            elif WorkoutStep._str_is_distance(duration):
                return WorkoutStep._str_to_meters(duration)
            elif WorkoutStep._str_is_calories(duration):
                return WorkoutStep._str_to_calories(duration)
            elif WorkoutStep._str_is_ppm(duration):
                return WorkoutStep._str_to_ppm(duration)
        return int(0)

    @staticmethod
    def _str_is_time(string):
        return True if ':' in string else False

    @staticmethod
    def _str_to_seconds(time_string):
        return Duration(str(time_string)).to_seconds()

    @staticmethod
    def _str_is_distance(string):
        return True if 'm' in string.lower() else False

    @staticmethod
    def _str_to_meters(string):
        if 'km' in string.lower():
            return float(string.lower().split('km')[0])*1000.0
        return float(string.lower().split('m')[0])

    @staticmethod
    def _str_is_calories(string):
        return True if 'cals' in string else False

    @staticmethod
    def _str_to_calories(string):
        return float(string.lower().split('cals')[0])

    @staticmethod
    def _str_is_ppm(string):
        return True if 'ppm' in string else False

    @staticmethod
    def _str_to_ppm(string):
        return float(string.lower().split('ppm')[0])

    @staticmethod
    def parsed_end_condition_value(end_condition_value):
        if end_condition_value:
            if "m" in end_condition_value:
                # Heart zones
                if 'ppm' in end_condition_value:
                    return int(end_condition_value.split('ppm')[0])
                # distance
                elif end_condition_value.endswith("km"):
                    return int(float(end_condition_value.replace("km", "")) * 1000)
                else:
                    return int(end_condition_value.replace("m", ""))
            # time
            elif ":" in end_condition_value:
                return Duration(end_condition_value).to_seconds()
            # calories
            elif end_condition_value and "cals" in end_condition_value:
                return int(end_condition_value.replace("cals", ""))
        else:
            return None

    def create_workout_step(self):
        return {
            "type": "ExecutableStepDTO",
            "stepId": None,
            "stepOrder": self.order,
            "childStepId": self.child_step_id,
            "description": self.description,
            _STEP_TYPE_FIELD: get_step_type(self.step_type),
            _END_CONDITION_FIELD: get_end_condition(self.end_condition),
            "preferredEndConditionUnit": WorkoutStep.end_condition_unit(self.end_condition),
            f"{_END_CONDITION_FIELD}Value": WorkoutStep.parsed_end_condition_value(self.end_condition_value),
            f"{_END_CONDITION_FIELD}Compare": None,
            f"{_END_CONDITION_FIELD}Zone": None,
            "category": self.category[0],
            "exerciseName": self.exerciseName[0],
            **self.target.create_target(),
            **self.secondary_target.create_target(),
            **get_stroke_type(self.stroke),
            **get_equipment_type(self.equipment),
            **get_weight(self.weight[0])
        }
