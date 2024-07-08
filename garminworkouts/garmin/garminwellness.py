from datetime import date
from garminworkouts.garmin.garminbiometric import GarminBiometric


class GarminWellness(GarminBiometric):
    _WELLNESS_SERVICE_ENDPOINT = "/wellness-service"

    def get_RHR(self) -> int:
        url: str = f"{self._WELLNESS_SERVICE_ENDPOINT}/wellness/dailyHeartRate"
        params: dict = {
            "date": date.today(),
        }
        response: str = self.get(url, params=params).json().get('restingHeartRate', '')

        return int(response)
