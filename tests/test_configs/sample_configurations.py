import os
from garminworkouts.models.settings import settings


class Arg(object):
    def __init__(
        self,
        trainingplan
    ) -> None:
        self.trainingplan: str = trainingplan


args = Arg(trainingplan=os.path.join('.', 'tests', 'test_configs', '*.yaml'))
workouts, notes, events, plan = settings(args)
