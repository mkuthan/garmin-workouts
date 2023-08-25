from dataclasses import dataclass
from garminworkouts.models.time import Time


@dataclass(frozen=True)
class Pace:
    pace: str

    def to_seconds(self) -> int:
        t: int = Time(self.pace).to_seconds()
        return t if t > 20 else 20

    def to_speed(self) -> float:
        return 1000.0 / self.to_seconds()

    def to_pace(self, vVO2=str('3:00'), diff=float(0)) -> float:
        vVO2s: int = Time(vVO2).to_seconds()
        if not 0 <= Time(vVO2).to_seconds() < 1000:
            raise ValueError('vVO2 must be between 0 [s] and 500 [s] but was %s' % vVO2s)

        if self._has_time():
            absolute_pace: float = Pace(self.pace).to_speed()
        elif self._has_percent():
            absolute_pace = self._to_absolute(Pace(vVO2).to_speed(), float(self.pace[:-1]))
        else:
            absolute_pace = self._to_absolute(Pace(vVO2).to_speed(), float(self.pace)*100)

        return 1.0/(1.0/absolute_pace + diff/1000)

    def _has_time(self) -> bool:
        return ':' in self.pace

    def _has_percent(self) -> bool:
        return (self.pace.lower()).endswith('%')

    @staticmethod
    def _to_absolute(pace, vVO2) -> float:
        return float(pace) * float(vVO2)/100
