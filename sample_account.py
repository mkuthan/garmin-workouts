# save this as account.py
from datetime import date
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power

USERNAME = 'enter username here'
PASSWORD = 'enter password here'
locale = 'en-US'
race = date(2023, 7, 5)
vV02 = Pace('5:00')
fmin = int(60)
fmax = int(200)
rFTP = Power('400w')
cFTP = Power('300w')
