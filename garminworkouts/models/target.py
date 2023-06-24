from garminworkouts.models.fields import get_target_type, get_target_fields


class Target:
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

    def create_target(self):
        if self.target == 'no.target':
            return {}
        else:
            target, zone = get_target_fields(self.secondary)
            return {
                f"{target}Type": get_target_type(self.target),
                f"{target}ValueOne": self.to_value,
                f"{target}ValueTwo": self.from_value,
                f"{zone}Number": self.zone,
                }
