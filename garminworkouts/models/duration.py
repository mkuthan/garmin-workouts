from dataclasses import dataclass
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
        if type == 'heart.rate':
            return f"{value}ppm"
        elif type == 'distance':
            if value >= 100:
                return f"{value}m"
            else:
                return f"{value}km"
        elif type == 'calories':
            return f"{value}cals"
        elif type == 'reps':
            return f"{value}reps"
        elif type == 'power':
            return f"{value}w"
        elif type == 'time':
            return Time.to_str(value)
        else:
            return ''

    @staticmethod
    def get_value(duration: str) -> int | None:
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
