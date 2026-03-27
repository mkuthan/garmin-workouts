from dataclasses import dataclass


@dataclass(frozen=True)
class Duration:
    duration: str

    def to_seconds(self):
        if self._has_hours():
            hours, minutes, seconds = self._tokenize()
            return self._to_seconds(seconds, minutes, hours)
        elif self._has_minutes():
            minutes, seconds = self._tokenize()
            return self._to_seconds(seconds, minutes)
        elif self._has_seconds():
            [seconds] = self._tokenize()
            return self._to_seconds(seconds)
        else:
            raise ValueError(f"Unknown duration {self.duration}, expected format HH:MM:SS")

    def _tokenize(self):
        return self.duration.split(":")

    def _has_seconds(self):
        return len(self._tokenize()) == 1

    def _has_minutes(self):
        return len(self._tokenize()) == 2

    def _has_hours(self):
        return len(self._tokenize()) == 3

    @staticmethod
    def _to_seconds(seconds, minutes=0, hours=0):
        if not 0 <= int(seconds) < 60:
            raise ValueError(f"Seconds must be between 0 and 59 but was {seconds}")
        if not 0 <= int(minutes) < 60:
            raise ValueError(f"Minutes must be between 0 and 59 but was {seconds}")
        if not 0 <= int(hours) < 24:
            raise ValueError(f"Hours must be between 0 and 23 but was {seconds}")

        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
