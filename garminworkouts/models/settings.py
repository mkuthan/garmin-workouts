import glob
import account
import os
from garminworkouts.config import configreader
from datetime import date
from garminworkouts.models.workout import Workout
from garminworkouts.models.note import Note


def settings(args):
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
    combined: list[Workout | Note] = [Workout(workout_config,
                                              target,
                                              account.vV02,
                                              account.fmin,
                                              account.fmax,
                                              account.flt,
                                              account.rFTP,
                                              account.cFTP,
                                              plan,
                                              race) if 'content' in workout_config else Note(workout_config)
                                      for workout_config in workout_configs]

    notes = [w for w in combined if isinstance(w, Note)]
    workouts = [w for w in combined if isinstance(w, Workout)]

    return workouts, notes, plan
