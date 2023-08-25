from dataclasses import dataclass
from garminworkouts.models.time import Time


@dataclass(frozen=True)
class Duration:
    duration: str

    def get_type(self) -> str:
        if self.duration:
            if Duration.is_heart_rate(self.duration):
                return 'heart.rate'
            elif Duration.is_distance(self.duration):
                return 'distance'
            elif Duration.is_energy(self.duration):
                return 'calories'
            elif Duration.is_reps(self.duration):
                return 'reps'
            elif Duration.is_power(self.duration):
                return 'power'
            elif Duration.is_time(self.duration):
                return 'time'
        return 'lap.button'

    @staticmethod
    def get_value(duration: str) -> int | None:
        if 'ppm' in duration:
            return int(duration.split('ppm')[0])
        elif 'km' in duration:
            return int(float(duration.split('km')[0]) * 1000)
        elif 'm' in duration:
            return int(float(duration.split('m')[0]))
        elif 'cals' in duration:
            return int(float(duration.split('cals')[0]))
        elif 'reps' in duration:
            return int(duration.split('reps')[0])
        elif ':' in duration:
            return Time(duration).to_seconds()

    @staticmethod
    def is_time(string: str) -> bool:
        return True if ':' in string else False

    @staticmethod
    def is_distance(string: str) -> bool:
        return True if 'm' in string.lower() else False

    @staticmethod
    def is_reps(string: str) -> bool:
        return True if 'reps' in string.lower() else False

    @staticmethod
    def is_heart_rate(string: str) -> bool:
        return True if 'ppm' in string.lower() else False

    @staticmethod
    def is_power(string: str) -> bool:
        return True if 'w' in string.lower() else False

    @staticmethod
    def is_energy(string: str) -> bool:
        return True if 'cals' in string.lower() else False

    def to_seconds(self) -> int:
        return Time(self.duration).to_seconds()
