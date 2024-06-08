from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class Time:
    duration: str

    def to_seconds(self) -> int:
        try:
            hours, minutes, seconds = map(int, self.duration.split(':'))
        except ValueError:
            hours = 0
            try:
                minutes, seconds = map(int, self.duration.split(':'))
            except ValueError:
                minutes = 0
                seconds = int(self.duration)
        if hours < 0 or hours > 23:
            raise ValueError('Invalid duration')
        if minutes < 0 or minutes > 59:
            raise ValueError('Invalid duration')
        if seconds < 0 or seconds > 59:
            raise ValueError('Invalid duration')
        return hours * 3600 + minutes * 60 + seconds

    @staticmethod
    def to_str(seconds: int) -> str:
        return str(timedelta(seconds=seconds))
