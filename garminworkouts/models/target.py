from garminworkouts.models.fields import get_target_type, get_target_fields, TARGET_TYPES
import numbers


class Target:
    def __init__(
            self,
            target='no.target',
            value_one=None,
            value_two=None,
            zone=None,
            secondary=False,
    ):

        self.target = target
        self.value_one = value_one if target != 'no.target' else None
        self.value_two = value_two if target != 'no.target' else None
        self.zone = zone if target == 'heart.rate.zone' else None
        self.secondary = secondary

        if target not in TARGET_TYPES.keys():
            raise TypeError(' %s Undefined target type' % target)
        if not isinstance(target, str):
            raise TypeError('Target %s needs to be in str format' % target)
        if target != 'no.target' and not isinstance(self.value_one, numbers.Number):
            raise TypeError('Value One %s needs to be in numeric format' % self.value_one)
        if target != 'no.target' and not isinstance(self.value_two, numbers.Number):
            raise TypeError('Value One %s needs to be in numeric format' % self.value_two)
        if (target != 'no.target' and self.value_one and self.value_two and
           self.value_two <= self.value_one and target != 'pace.zone'):  # type: ignore
            raise TypeError('Value One %s needs to be smaller or equal than Value Two %s'
                            % (self.value_one, self.value_two))
        if (target != 'no.target' and self.value_one and self.value_two and
           self.value_two > self.value_one and target == 'pace.zone'):  # type: ignore
            raise TypeError('Value Two %s needs to be smaller or equal than Value One %s'
                            % (self.value_one, self.value_two))
        if not isinstance(self.secondary, bool):
            raise TypeError('Secondary %s needs to be in bool format' % self.secondary)
        if target == 'heart.rate.zone':
            if (self.value_one and self.value_two and self.zone and
               (self.zone < 1 and self.zone > 5)):  # type: ignore
                raise TypeError('Zone %s needs to be in bool format is undefined' % self.zone)

    def create_target(self):
        if self.target == 'no.target':
            return {}
        else:
            target, zone = get_target_fields(self.secondary)
            return {
                f'{target}Type': get_target_type(self.target),
                f'{target}ValueOne': self.value_one,
                f'{target}ValueTwo': self.value_two,
                f'{zone}Number': self.zone,
                }
