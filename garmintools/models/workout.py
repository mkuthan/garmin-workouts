_WORKOUT_ID_FIELD = "workoutId"
_WORKOUT_NAME_FIELD = "workoutName"

_CYCLING_SPORT_TYPE = {
    "sportTypeId": 2,
    "sportTypeKey": "cycling"
}

_INTERVAL_STEP_TYPE = {
    "stepTypeId": 3,
    "stepTypeKey": "interval",
}

_POWER_TARGET_DIFF = 0.05


def build_cycling_workout(workout_config, ftp, power_target_diff=_POWER_TARGET_DIFF):
    return {
        _WORKOUT_NAME_FIELD: workout_config["name"],
        "description": workout_config.get("description"),
        "sportType": _CYCLING_SPORT_TYPE,
        "workoutSegments": [
            {
                "segmentOrder": 1,
                "sportType": _CYCLING_SPORT_TYPE,
                "workoutSteps": _steps(workout_config["steps"], ftp, power_target_diff)
            }
        ]
    }


def get_workout_id(workout):
    return workout[_WORKOUT_ID_FIELD]


def get_workout_name(workout):
    return workout[_WORKOUT_NAME_FIELD]


def _steps(steps_config, ftp, power_target_diff):
    steps_config_flat = [item for sublist in steps_config for item in sublist]
    return [_step(step_config, i, ftp, power_target_diff) for i, step_config in enumerate(steps_config_flat)]


def _step(step_config, i, ftp, power_target_diff):
    return {
        "type": "ExecutableStepDTO",
        "stepOrder": i + 1,
        "description": step_config.get("description"),
        "stepType": _INTERVAL_STEP_TYPE,
        "endCondition": _end_condition(step_config),
        "endConditionValue": _end_condition_value(step_config),
        "targetType": _target_type(step_config),
        "targetValueOne": _target_value(step_config, ftp, -power_target_diff),
        "targetValueTwo": _target_value(step_config, ftp, +power_target_diff)
    }


def _get_duration(step_config):
    return step_config.get("duration")


def _end_condition(step_config):
    duration = _get_duration(step_config)
    type_id = 2 if duration else 1
    type_key = "time" if duration else "lap.button"
    return {
        "conditionTypeId": type_id,
        "conditionTypeKey": type_key
    }


def _end_condition_value(step_config):
    duration = _get_duration(step_config)
    return _calculate_duration(duration) if duration else None


def _calculate_duration(duration):
    (minutes, seconds) = duration.split(":")
    return int(minutes) * 60 + int(seconds)


def _get_power(step):
    return step.get("power")


def _target_type(step_config):
    power = _get_power(step_config)
    type_id = 2 if power else 1
    type_key = "power.zone" if power else "no.target"
    return {
        "workoutTargetTypeId": type_id,
        "workoutTargetTypeKey": type_key
    }


def _target_value(step_config, ftp, power_target_diff):
    power = _get_power(step_config)
    return _calculate_power(ftp, power, power_target_diff) if power else None


def _calculate_power(ftp, power, diff):
    final_power = int(power) * (1 + diff)
    return round(final_power * ftp / 100)
