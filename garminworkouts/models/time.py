from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class Time:
    duration: str

    def to_seconds(self) -> int:
        if Time._has_hours(self.duration):
            hours, minutes, seconds = Time.time_tokenize(self.duration)
            return Time._to_seconds(int(seconds), int(minutes), int(hours))
        elif Time._has_minutes(self.duration):
            minutes, seconds = Time.time_tokenize(self.duration)
            return Time._to_seconds(int(seconds), int(minutes))
        elif Time._has_seconds(self.duration):
            [seconds] = Time.time_tokenize(self.duration)
            return Time._to_seconds(int(seconds))
        else:
            raise ValueError('Unknown duration %s, expected format HH:MM:SS' % self.duration)

    @staticmethod
    def to_str(seconds: int) -> str:
        return str(timedelta(seconds=seconds))

    @staticmethod
    def time_tokenize(duration: str) -> list[str]:
        return duration.split(':')

    @staticmethod
    def _has_seconds(duration: str) -> bool:
        if 'km' not in duration:
            return len(Time.time_tokenize(duration)) == 1
        else:
            return bool(0)

    @staticmethod
    def _has_minutes(duration: str) -> bool:
        return len(Time.time_tokenize(duration)) == 2

    @staticmethod
    def _has_hours(duration: str) -> bool:
        return len(Time.time_tokenize(duration)) == 3

    @staticmethod
    def _to_seconds(seconds: int, minutes=int(0), hours=int(0)) -> int:
        if not 0 <= int(seconds) < 60:
            raise ValueError('Seconds must be between 0 and 59 but was %s' % seconds)
        if not 0 <= int(minutes) < 60:
            raise ValueError('Minutes must be between 0 and 59 but was %s' % seconds)
        if not 0 <= int(hours) < 24:
            raise ValueError('Hours must be between 0 and 23 but was %s' % seconds)

        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
