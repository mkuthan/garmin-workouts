from dataclasses import dataclass
from typing import List, Dict


@dataclass(frozen=True)
class Power:
    power: str

    def to_watts(self, ftp: int) -> float:
        ftp = int(ftp)
        if not 0 <= ftp < 1000:
            raise ValueError('FTP must be between 0 [W] and 999 [W] but was %s' % ftp)

        if self._has_watt():
            absolute_power = int(self.power[:-1])
        elif self._has_percent():
            absolute_power: float = self._to_absolute(int(self.power[:-1]), ftp)
        else:
            absolute_power = self._to_absolute(int(self.power), ftp)

        if not 0 <= absolute_power < 5000:
            raise ValueError('Power must be between 0 [W] and 49999 [W] but was %s' % absolute_power)

        return round(absolute_power)

    def _has_watt(self) -> bool:
        return self.power.lower().endswith('w')

    def _has_percent(self) -> bool:
        return self.power.lower().endswith('%')

    @staticmethod
    def _to_absolute(power: int, ftp: int) -> float:
        return power * ftp / 100

    @staticmethod
    def power_zones(rftp, cftp) -> tuple[List[float], List[int], List[int], List[Dict]]:
        zones: List[float] = [0.65, 0.8, 0.9, 1.0, 1.15, 1.3, 1.5, 1.7]
        rpower_zones: List[int] = [int(rftp.to_watts(int(rftp.power[:-1])) * zone) for zone in zones]
        cpower_zones: List[int] = [int(cftp.to_watts(int(cftp.power[:-1])) * zone) for zone in zones]

        data: list[dict] = [
            {
                'sport': 'CYCLING',
                'functionalThresholdPower': cftp.power[:-1],
                'zone1Floor': str(cpower_zones[0]),
                'zone2Floor': str(cpower_zones[1]),
                'zone3Floor': str(cpower_zones[2]),
                'zone4Floor': str(cpower_zones[3]),
                'zone5Floor': str(cpower_zones[4]),
                'zone6Floor': str(cpower_zones[5]),
                'zone7Floor': str(cpower_zones[6]),
                'userLocalTime': None
            },
            {
                'sport': 'RUNNING',
                'functionalThresholdPower': rftp.power[:-1],
                'zone1Floor': str(rpower_zones[1]),
                'zone2Floor': str(rpower_zones[2]),
                'zone3Floor': str(rpower_zones[3]),
                'zone4Floor': str(rpower_zones[4]),
                'zone5Floor': str(rpower_zones[5]),
                'zone6Floor': str(0.0),
                'zone7Floor': str(0.0),
                'userLocalTime': None
            }
        ]

        return zones, rpower_zones, cpower_zones, data
