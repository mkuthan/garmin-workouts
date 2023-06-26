
from garminworkouts.models.settings import settings


class Arg(object):
    def __init__(
        self,
        workout
    ):
        self.workout = workout


args = Arg(workout='./test_configs/*.yaml')
workout, plan = settings(args)
