import glob
import account
import os
from garminworkouts.config import configreader
from datetime import date
from garminworkouts.models.workout import Workout


def settings(args) -> tuple[list[Workout], str]:
    if isinstance(args.workout, tuple):
        args.workout = ''.join(args.workout)

    workout_files: list[str] = glob.glob(args.workout)
    plan = str('')
    race: date = date.today()
    try:
        planning: dict = configreader.read_config(os.path.join('.', 'events', 'planning', 'planning.yaml'))
    except FileNotFoundError:
        print('Planning does not exist')
        planning = {}

    if not workout_files:
        try:
            workout_files = glob.glob(planning[args.workout]['workouts'])
            race = date(planning[args.workout]['year'], planning[args.workout]['month'], planning[args.workout]['day'])
            plan: str = args.workout
        except KeyError:
            if 'year' in planning[args.workout]:
                print(args.workout + ' not found in planning, please check "planning.yaml"')

    workout_configs: list = [configreader.read_config(workout_file) for workout_file in workout_files]
    target: dict = configreader.read_config(r'target.yaml')
    workouts: list[Workout] = [Workout(workout_config,
                                       target,
                                       account.vV02,
                                       account.fmin,
                                       account.fmax,
                                       account.rFTP,
                                       account.cFTP,
                                       plan,
                                       race)
                               for workout_config in workout_configs]

    return workouts, plan
