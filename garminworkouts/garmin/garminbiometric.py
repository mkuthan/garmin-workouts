from datetime import date
from requests import Response
import account
from garminworkouts.garmin.garmintypes import GarminTypes
from garminworkouts.models.power import Power
from garminworkouts.models.workout import Workout


class GarminBiometric(GarminTypes):
    _BIOMETRIC_SERVICE_ENDPOINT = "/biometric-service"

    def get_hr_zones(self) -> dict:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
        return self.get(url).json()

    def save_hr_zones(self, zones) -> Response:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
        return self.put(url, json=zones)

    def get_power_zones(self) -> dict:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/sports/all"
        return self.get(url).json()

    def save_power_zones(self, zones) -> Response:
        url: str = f"{self._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/all"
        return self.put(url, json=zones)

    def user_zones(self) -> None:
        _, _, data = Workout(
            [],
            [],
            account.vV02,
            account.fmin,
            account.fmax,
            account.flt,
            account.rFTP,
            account.cFTP,
            str(''),
            date.today()).hr_zones()

        _, _, _, pdata = Power.power_zones(account.rFTP, account.cFTP)

        self.save_hr_zones(data)
        self.save_power_zones(pdata)

        Workout([],
                [],
                account.vV02,
                account.fmin,
                account.fmax,
                account.flt,
                account.rFTP,
                account.cFTP,
                str(''),
                date.today()
                ).zones()
