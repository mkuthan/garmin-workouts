from dataclasses import dataclass


@dataclass(frozen=True)
class Power:
    power: str

    def to_watts(self, ftp, diff=0):
        if not 0 <= int(ftp) < 1000:
            raise ValueError("FTP must be between 0 [W] and 999 [W] but was %s" % ftp)

        if not -1.0 < float(diff) < 1.0:
            raise ValueError("Power diff must be between -0.99 and 0.99 but was %s" % diff)

        if self._has_watt():
            absolute_power = int(self.power[:-1])
        elif self._has_percent():
            absolute_power = self._to_absolute(self.power[:-1], ftp)
        else:
            absolute_power = self._to_absolute(self.power, ftp)

        if not 0 <= int(absolute_power) < 5000:
            raise ValueError("Power must be between 0 [W] and 49999 [W] but was %s" % absolute_power)

        return round(absolute_power * (1 + diff))

    def _has_watt(self):
        return self.power.lower().endswith("w")

    def _has_percent(self):
        return self.power.lower().endswith("%")

    @staticmethod
    def _to_absolute(power, ftp):
        return int(power) * ftp / 100
