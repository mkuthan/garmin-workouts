from dataclasses import dataclass


@dataclass(frozen=True)
class Duration:
    duration: str

    def to_seconds(self):
        if self._has_hours():
            hours, minutes, seconds = self._tokenize()
            return self._to_seconds(seconds, minutes, hours) # type: ignore
        elif self._has_minutes():
            minutes, seconds = self._tokenize()
            return self._to_seconds(seconds, minutes) # type: ignore
        elif self._has_seconds():
            [seconds] = self._tokenize()
            return self._to_seconds(seconds)
        else:
            raise ValueError("Unknown duration %s, expected format HH:MM:SS" % self.duration)

    def _tokenize(self):
        return self.duration.split(":")

    def _has_seconds(self):
        if not 'km' in self.duration:
            return len(self._tokenize()) == 1
        else:
            return 0

    def _has_minutes(self):
        return len(self._tokenize()) == 2

    def _has_hours(self):
        return len(self._tokenize()) == 3

    @staticmethod
    def _to_seconds(seconds, minutes=0, hours=0):
        if not 0 <= int(seconds) < 60:
            raise ValueError("Seconds must be between 0 and 59 but was %s" % seconds)
        if not 0 <= int(minutes) < 60:
            raise ValueError("Minutes must be between 0 and 59 but was %s" % seconds)
        if not 0 <= int(hours) < 24:
            raise ValueError("Hours must be between 0 and 23 but was %s" % seconds)

        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
