from dataclasses import dataclass
from typing import Union
from garminworkouts.models.time import Time
from garminworkouts.models.types import TYPE_MAPPING


@dataclass(frozen=True)
class Duration:
    duration: str

    def get_type(self) -> str:
        for key, value in TYPE_MAPPING.items():
            if key in self.duration:
                return value
        if Duration.is_time(self.duration):
            return 'time'
        return 'lap.button'

    @staticmethod
    def get_string(value: int, type: str) -> str:
        type_mapping: dict = {
            'heart.rate': f"{value}ppm",
            'distance': f"{value}m" if value >= 100 else f"{value}km",
            'calories': f"{value}cals",
            'reps': f"{value}reps",
            'power': f"{value}w",
            'time': Time.to_str(value)
        }
        return type_mapping.get(type, '')

    @staticmethod
    def get_value(duration: str) -> Union[int, None]:
        for key in TYPE_MAPPING.keys():
            if key in duration:
                return int(float(duration.split(key)[0]) if key != 'reps' else duration.split(key)[0])
        if ':' in duration:
            return Time(duration).to_seconds()

    @staticmethod
    def is_time(string: str) -> bool:
        return ':' in string

    @staticmethod
    def is_distance(string: str) -> bool:
        return 'm' in string or 'km' in string

    @staticmethod
    def is_reps(string: str) -> bool:
        return 'reps' in string

    @staticmethod
    def is_heart_rate(string: str) -> bool:
        return 'ppm' in string

    @staticmethod
    def is_power(string: str) -> bool:
        return 'w' in string

    @staticmethod
    def is_energy(string: str) -> bool:
        return 'cals' in string

    def to_seconds(self) -> int:
        return Time(self.duration).to_seconds()
