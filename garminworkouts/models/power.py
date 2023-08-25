from dataclasses import dataclass


@dataclass(frozen=True)
class Power:
    power: str

    def to_watts(self, ftp) -> float:
        if not 0 <= int(ftp) < 1000:
            raise ValueError('FTP must be between 0 [W] and 999 [W] but was %s' % ftp)

        if self._has_watt():
            absolute_power = int(self.power[:-1])
        elif self._has_percent():
            absolute_power: float = self._to_absolute(self.power[:-1], ftp)
        else:
            absolute_power = self._to_absolute(self.power, ftp)

        if not 0 <= int(absolute_power) < 5000:
            raise ValueError('Power must be between 0 [W] and 49999 [W] but was %s' % absolute_power)

        return float(round(absolute_power))

    def _has_watt(self) -> bool:
        return (self.power.lower()).endswith('w')

    def _has_percent(self) -> bool:
        return (self.power.lower()).endswith('%')

    @staticmethod
    def _to_absolute(power, ftp) -> float:
        return int(power) * ftp / 100

    @staticmethod
    def power_zones(zones: list[float], ftp) -> None:
        power_zones: list[int] = [round(int(ftp.to_watts()) * zone) for zone in zones]
        print('::Power Zones::')
        for i in range(len(zones)-1):
            print('Zone ', i, ': ', power_zones[i], '-', power_zones[i + 1])
