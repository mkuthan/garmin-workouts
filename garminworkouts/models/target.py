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

    def __init__(
            self,
            target="no.target",
            to_value=None,
            from_value=None,
            zone=None
            ):

        self.target = target
        self.to_value = to_value
        self.from_value = from_value
        self.zone = zone

    @staticmethod
    def get_target_type(target_type):
        return {
            "workoutTargetTypeId": TARGET_TYPES[target_type],
            "workoutTargetTypeKey": target_type,
            }

    def create_target(self):
        return {
            "targetType": {
                "workoutTargetTypeId": TARGET_TYPES[self.target],
                "workoutTargetTypeKey": self.target,
            },
            "targetValueOne": self.to_value,
            "targetValueTwo": self.from_value,
            "zoneNumber": self.zone,
        }

    def create_secondary_target(self):
        if self.target == 'no.target':
            return {}
        else:
            return {
                "secondaryTargetType": {
                    "workoutTargetTypeId": TARGET_TYPES[self.target],
                    "workoutTargetTypeKey": self.target,
                },
                "secondaryTargetValueOne": self.to_value,
                "secondaryTargetValueTwo": self.from_value,
                "secondaryZoneNumber": self.zone,
            }
