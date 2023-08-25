
from garminworkouts.models.settings import settings


class Arg(object):
    def __init__(
        self,
        workout
    ) -> None:
        self.workout = workout


args = Arg(workout='./tests/test_configs/*.yaml')
workouts, plan = settings(args)
