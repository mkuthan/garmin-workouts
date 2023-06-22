
from garminworkouts.models.duration import Duration
from garminworkouts.models.target import Target

STEP_TYPES = {
    "warmup": 1,
    "cooldown": 2,
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
        exerciseName=None
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

    def end_condition_unit(self):
        if self.end_condition and self.end_condition.endswith("km"):
            return {"unitKey": "kilometer"}
        else:
            return None

    def parsed_end_condition_value(self):
        # distance
        if self.end_condition_value and "m" in self.end_condition_value:
            if self.end_condition_value.endswith("km"):
                return int(float(self.end_condition_value.replace("km", "")) * 1000)
            else:
                return int(self.end_condition_value.replace("m", ""))

        # time
        elif self.end_condition_value and ":" in self.end_condition_value:
            return Duration(self.end_condition_value).to_seconds()
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
            "preferredEndConditionUnit": self.end_condition_unit(),
            "endConditionValue": self.parsed_end_condition_value(),
            "endConditionCompare": None,
            "endConditionZone": None,
            "category": self.category[0],
            "exerciseName": self.exerciseName,
            **self.target.create_target(),
            **self.secondary_target.create_secondary_target(),
            **self.stroke(),
            **self.equipment(),
        }
