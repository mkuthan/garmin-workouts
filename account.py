from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from garminworkouts.garmin.garminclient import GarminClient
from decouple import config

USERNAME: str | bool = config('GARMIN_USERNAME')
PASSWORD: str | bool = config('GARMIN_PASSWORD')
locale = 'en-US'
vV02 = Pace(config('vV02'))  # type: ignore


def _garmin_client() -> GarminClient:
    return GarminClient(
            connect_url="https://connect.garmin.com",
            sso_url="https://sso.garmin.com",
            username=USERNAME,
            password=PASSWORD,
            cookie_jar=".garmin-cookies.txt"
        )


with _garmin_client() as connection:
    try:
        fmin: int = connection.get_RHR()
    except Exception:
        fmin = int(config('fmin'))

fmax = int(config('fmax'))
flt = int(config('flt'))
rFTP = Power(config('rFTP'))  # type: ignore
cFTP = Power(config('cFTP'))  # type: ignore
BOT_TOKEN: str | bool = config('BOT_TOKEN')
