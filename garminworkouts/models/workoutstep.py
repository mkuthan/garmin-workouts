
from garminworkouts.models.duration import Duration
from garminworkouts.models.power import Power
from garminworkouts.models.target import Target

STEP_TYPES = {
    "warmup": 1,
    "cooldown": 2,
    "run": 3,
    "interval": 3,
    "recovery": 4,
    "rest": 5,
    "repeat": 6,
    "other": 7
}

END_CONDITIONS = {
    "lap.button": 1,
    "time": 2,
    "distance": 3,
    "calories": 4,
    "iterations": 7,
    "fixed.rest": 8,
    "fixed.repetition": 9,
    "training.peaks.tss": 11,
    "repetition.time": 12,
    "time.at.valid.cda": 13,
    "power.last.lap": 14,
    "max.power.last.lap": 15,
    "reps": 10,
    "power": 5,         # Potencia por encima de un umbral ("endConditionCompare": "gt")
                        # Potencia por debajo de un umbral ("endConditionCompare": "lt")
    "heart.rate": 6,    # Pulsaciones por encima de un umbral ("endConditionCompare": "lt")
                        # Pulsaciones por debajo de un umbral ("endConditionCompare": "gt")
}


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
        self.exerciseName = exerciseName
        self.weight = weight

    @staticmethod
    def _get_duration(step):
        duration = step.get("duration")
        return Duration(str(duration)) if duration else None

    @staticmethod
    def _get_power(step):
        power = step.get("power")
        return Power(str(power)) if power else None

    @staticmethod
    def get_step_type(step_type):
        return {
                "stepTypeId": STEP_TYPES[step_type],
                "stepTypeKey": step_type,
            }

    @staticmethod
    def get_end_condition(end_condition):
        return {
                "conditionTypeId": END_CONDITIONS[end_condition],
                "conditionTypeKey": end_condition,
            }

    @staticmethod
    def end_condition_unit(end_condition):
        if end_condition and end_condition.endswith("km"):
            return {"unitKey": "kilometer"}
        else:
            return None

    @staticmethod
    def _end_condition(step_config):
        duration = step_config.get("duration")
        if duration:
            if WorkoutStep._str_is_time(duration):
                return WorkoutStep.get_end_condition("time")
            elif WorkoutStep._str_is_distance(duration):
                return WorkoutStep.get_end_condition("distance")
        return WorkoutStep.get_end_condition("lap.button")

    @staticmethod
    def _end_condition_value(step_config):
        duration = step_config.get("duration")
        if duration:
            if WorkoutStep._str_is_time(duration):
                return WorkoutStep._str_to_seconds(duration)
            if WorkoutStep._str_is_distance(duration):
                return WorkoutStep._str_to_meters(duration)
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
    def _str_to_meters(distance_string):
        if 'km' in distance_string.lower():
            return float(distance_string.lower().split('km')[0])*1000.0
        return float(distance_string.lower().split('m')[0])

    @staticmethod
    def _weight(weight):
        return {
            "weightValue": weight,
            "weightUnit": {
                "unitId": 8,
                "unitKey": "kilogram",
                "factor": 1000.0
            }
        }

    @staticmethod
    def parsed_end_condition_value(end_condition_value):
        # distance
        if end_condition_value and "m" in end_condition_value:
            if end_condition_value.endswith("km"):
                return int(float(end_condition_value.replace("km", "")) * 1000)
            else:
                return int(end_condition_value.replace("m", ""))

        # time
        elif end_condition_value and ":" in end_condition_value:
            return Duration(end_condition_value).to_seconds()
        else:
            return None

    def stroke(self):
        return {
            "strokeType": {
                "strokeTypeId": 0,
                "displayOrder": 0
            }
        }

    def equipment(self):
        return {
            "equipmentType": {
                "equipmentTypeId": 0,
                "displayOrder": 0
            }
        }

    def create_workout_step(self):
        return {
            "type": "ExecutableStepDTO",
            "stepId": None,
            "stepOrder": self.order,
            "childStepId": self.child_step_id,
            "description": self.description,
            "stepType": {
                "stepTypeId": STEP_TYPES[self.step_type],
                "stepTypeKey": self.step_type,
            },
            "endCondition": {
                "conditionTypeKey": self.end_condition,
                "conditionTypeId": END_CONDITIONS[self.end_condition],
            },
            "preferredEndConditionUnit": WorkoutStep.end_condition_unit(self.end_condition),
            "endConditionValue": WorkoutStep.parsed_end_condition_value(self.end_condition_value),
            "endConditionCompare": None,
            "endConditionZone": None,
            "category": self.category[0],
            "exerciseName": self.exerciseName,
            **self.target.create_target(),
            **self.secondary_target.create_secondary_target(),
            **self.stroke(),
            **self.equipment(),
            **self._weight(self.weight)
        }
