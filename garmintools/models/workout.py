class Workout(object):
    _WORKOUT_ID_FIELD = "workoutId"
    _WORKOUT_NAME_FIELD = "workoutName"
    _WORKOUT_OWNER_ID_FIELD = "ownerId"

    _CYCLING_SPORT_TYPE = {
        "sportTypeId": 2,
        "sportTypeKey": "cycling"
    }

    _INTERVAL_STEP_TYPE = {
        "stepTypeId": 3,
        "stepTypeKey": "interval",
    }

    _POWER_TARGET_DIFF = 0.05

    @staticmethod
    def create_cycling_workout(workout_config, ftp, power_target_diff=_POWER_TARGET_DIFF):
        workout_steps = Workout._steps(workout_config["steps"], ftp, power_target_diff)
        workout = {
            Workout._WORKOUT_NAME_FIELD: workout_config["name"],
            "description": workout_config.get("description"),
            "sportType": Workout._CYCLING_SPORT_TYPE,
            "workoutSegments": [
                {
                    "segmentOrder": 1,
                    "sportType": Workout._CYCLING_SPORT_TYPE,
                    "workoutSteps": workout_steps
                }
            ]
        }
        return Workout(workout)

    def __init__(self, workout):
        self.workout = workout

    def get_id(self):
        return self.workout[Workout._WORKOUT_ID_FIELD]

    def get_name(self):
        return self.workout[Workout._WORKOUT_NAME_FIELD]

    def get_owner_id(self):
        return self.workout[Workout._WORKOUT_OWNER_ID_FIELD]

    def update(self, other):
        self.workout[Workout._WORKOUT_ID_FIELD] = other.get_id()
        self.workout[Workout._WORKOUT_OWNER_ID_FIELD] = other.get_owner_id()

    @staticmethod
    def _steps(steps_config, ftp, power_target_diff):
        steps_config_flat = [item for sublist in steps_config for item in sublist]
        return [Workout._step(step_config, i, ftp, power_target_diff) for i, step_config in enumerate(steps_config_flat)]

    @staticmethod
    def _step(step_config, i, ftp, power_target_diff):
        return {
            "type": "ExecutableStepDTO",
            "stepOrder": i + 1,
            "description": step_config.get("description"),
            "stepType": Workout._INTERVAL_STEP_TYPE,
            "endCondition": Workout._end_condition(step_config),
            "endConditionValue": Workout._end_condition_value(step_config),
            "targetType": Workout._target_type(step_config),
            "targetValueOne": Workout._target_value(step_config, ftp, -power_target_diff),
            "targetValueTwo": Workout._target_value(step_config, ftp, +power_target_diff)
        }

    @staticmethod
    def _get_duration(step_config):
        return step_config.get("duration")

    @staticmethod
    def _end_condition(step_config):
        duration = Workout._get_duration(step_config)
        type_id = 2 if duration else 1
        type_key = "time" if duration else "lap.button"
        return {
            "conditionTypeId": type_id,
            "conditionTypeKey": type_key
        }

    @staticmethod
    def _end_condition_value(step_config):
        duration = Workout._get_duration(step_config)
        return Workout._calculate_duration(duration) if duration else None

    @staticmethod
    def _calculate_duration(duration):
        (minutes, seconds) = duration.split(":")
        return int(minutes) * 60 + int(seconds)

    @staticmethod
    def _get_power(step):
        return step.get("power")

    @staticmethod
    def _target_type(step_config):
        power = Workout._get_power(step_config)
        type_id = 2 if power else 1
        type_key = "power.zone" if power else "no.target"
        return {
            "workoutTargetTypeId": type_id,
            "workoutTargetTypeKey": type_key
        }

    @staticmethod
    def _target_value(step_config, ftp, power_target_diff):
        power = Workout._get_power(step_config)
        return Workout._calculate_power(ftp, power, power_target_diff) if power else None

    @staticmethod
    def _calculate_power(ftp, power, diff):
        final_power = int(power) * (1 + diff)
        return round(final_power * ftp / 100)
