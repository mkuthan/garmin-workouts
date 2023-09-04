import glob
import account
import os
from garminworkouts.config import configreader
from datetime import date
from garminworkouts.models.workout import Workout


def settings(args) -> tuple[list[Workout], str]:
    if isinstance(args.trainingplan, tuple):
        args.trainingplan = ''.join(args.trainingplan)

    workout_files: list[str] = glob.glob(args.trainingplan)
    plan = str('')
    race: date = date.today()
    try:
        planning: dict = configreader.read_config(os.path.join('.', 'events', 'planning', 'planning.yaml'))
    except FileNotFoundError:
        print('Planning does not exist')
        planning = {}

    if not workout_files:
        try:
            workout_files = glob.glob(planning[args.trainingplan]['workouts'])
            race = date(planning[args.trainingplan]['year'],
                        planning[args.trainingplan]['month'],
                        planning[args.trainingplan]['day'])
            plan: str = args.trainingplan
        except KeyError:
            os.path.exists(args.trainingplan)
            if '\\' not in args.trainingplan:
                if 'year' in planning[args.trainingplan]:
                    print(args.trainingplan + ' not found in planning, please check "planning.yaml"')

    workout_configs: list = [configreader.read_config(workout_file) for workout_file in workout_files]
    target: dict = configreader.read_config(r'target.yaml')
    workouts: list[Workout] = [Workout(workout_config,
                                       target,
                                       account.vV02,
                                       account.fmin,
                                       account.fmax,
                                       account.flt,
                                       account.rFTP,
                                       account.cFTP,
                                       plan,
                                       race)
                               for workout_config in workout_configs]

    return workouts, plan
