TARGET_TYPES = {
    "no.target": 1,
    "power.zone": 2,
    "cadence.zone": 3,
    "cadence": 3,
    "heart.rate.zone": 4,
    "speed.zone": 5,
    "pace.zone": 6,  # meters per second
    "grade": 7,
    "heart.rate.lap": 8,
    "power.lap": 9,
    "power.3s": 10,
    "power.10s": 11,
    "power.30s": 12,
    "speed.lap": 13,
    "swim.stroke": 14,
    "resistance": 15,
    "power.curve": 16
}


class Target:
    _WORKOUT_TARGET_FIELD = "workoutTargetType"

    def __init__(
            self,
            target="no.target",
            to_value=None,
            from_value=None,
            zone=None,
            secondary=False,
    ):

        self.target = target
        self.to_value = to_value
        self.from_value = from_value
        self.zone = zone
        self.secondary = secondary

    @staticmethod
    def get_target_type(target_type):
        return {
                f"{Target._WORKOUT_TARGET_FIELD}Id": TARGET_TYPES[target_type],
                f"{Target._WORKOUT_TARGET_FIELD}Key": target_type,
            } if target_type in TARGET_TYPES else {}

    def get_fields(self):
        target = 'target' if not self.secondary else 'secondaryTarget'
        zone = 'zone' if not self.secondary else 'secondaryZone'
        return target, zone

    def create_target(self):
        if self.target == 'no.target':
            return {}
        else:
            target, zone = self.get_fields()
            return {
                f"{target}Type": Target.get_target_type(self.target),
                f"{target}ValueOne": self.to_value,
                f"{target}ValueTwo": self.from_value,
                f"{zone}Number": self.zone,
                }
