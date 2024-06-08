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
            minutes, seconds = map(int, self.duration.split(':'))
        return hours * 3600 + minutes * 60 + seconds

    @staticmethod
    def to_str(seconds: int) -> str:
        return str(timedelta(seconds=seconds))
