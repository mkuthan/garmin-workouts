from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from decouple import config

USERNAME = config('GARMIN_USERNAME')
PASSWORD = config('PASSWORD')
locale = 'en-US'
vV02 = Pace(config('vV02'))  # type: ignore
fmin = int(config('fmin'))
fmax = int(config('fmax'))
rFTP = Power(config('rFTP'))  # type: ignore
cFTP = Power(config('cFTP'))  # type: ignore
BOT_TOKEN = config('BOT_TOKEN')
