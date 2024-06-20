from garminworkouts.models.fields import get_target_type, get_target_fields, TARGET_TYPES
import numbers
from typing import Any, Union


class Target:
    def __init__(
            self,
            target='no.target',
            value_one=None,
            value_two=None,
            zone=None,
            secondary=False,
    ) -> None:
        self.target: str = target
        self.value_one: Union[Any, None] = value_one if target != 'no.target' else None
        self.value_two: Union[Any, None] = value_two if target != 'no.target' else None
        self.zone: Union[Any, None] = zone if target in ['heart.rate.zone', 'power.zone'] else None
        self.secondary: bool = secondary

        if target not in TARGET_TYPES:
            raise TypeError(f'{target} Undefined target type')

        if target != 'no.target' and not isinstance(self.value_one, numbers.Number):
            raise TypeError(f'Value One {self.value_one} needs to be in numeric format')

        if target != 'no.target' and not isinstance(self.value_two, numbers.Number):
            raise TypeError(f'Value Two {self.value_two} needs to be in numeric format')

        if (target != 'no.target' and self.value_one and self.value_two and
           self.value_two <= self.value_one and target != 'pace.zone'):  # type: ignore
            raise TypeError('Value One %s needs to be smaller or equal than Value Two %s'
                            % (self.value_one, self.value_two))

        if (target != 'no.target' and self.value_one and self.value_two and
           self.value_two > self.value_one and target == 'pace.zone'):  # type: ignore
            raise TypeError('Value Two %s needs to be smaller or equal than Value One %s'
                            % (self.value_one, self.value_two))

        if target == 'heart.rate.zone':
            if self.zone and isinstance(self.zone, int) and (self.zone < 1 or self.zone > 5):
                raise TypeError(f'Zone {self.zone} needs to be in bool format is undefined')

    def create_target(self) -> Union[dict[Any, Any], dict[str, Any]]:
        if self.target == 'no.target':
            return {}
        else:
            return {
                f'{get_target_fields(self.secondary)[0]}Type': get_target_type(self.target),
                f'{get_target_fields(self.secondary)[0]}ValueOne': self.value_one,
                f'{get_target_fields(self.secondary)[0]}ValueTwo': self.value_two,
                f'{get_target_fields(self.secondary)[1]}Number': self.zone,
            }
