import glob
import account
import os
from garminworkouts.config import configreader
from datetime import date
from garminworkouts.models.workout import Workout
from garminworkouts.models.note import Note


def settings(args):
    try:
        planning: dict = configreader.read_config(os.path.join('.', 'events', 'planning', 'planning.yaml'))
    except FileNotFoundError:
        print('Planning is not defined')
        planning = {}

    if isinstance(args.trainingplan, tuple):
        args.trainingplan = ''.join(args.trainingplan)

    if args.trainingplan in planning:
        workout_files = glob.glob(planning[args.trainingplan]['workouts'])
        if 'year' in planning[args.trainingplan]:
            race = date(
                planning[args.trainingplan]['year'],
                planning[args.trainingplan]['month'],
                planning[args.trainingplan]['day']
                )
        else:
            race: date = date.today()
        plan: str = args.trainingplan
    elif os.path.isfile(args.trainingplan):
        workout_files: list[str] = glob.glob(args.trainingplan)
        plan = str('')
        race: date = date.today()
    else:
        print(args.trainingplan + ' not found in planning, please check "planning.yaml"')
        return [], [], ''

    try:
        workout_configs: list = [configreader.read_config(workout_file) for workout_file in workout_files]
        target: dict = configreader.read_config(r'target.yaml')
        combined: list[Workout | Note] = [
            Workout(
                workout_config,
                target,
                account.vV02,
                account.fmin,
                account.fmax,
                account.flt,
                account.rFTP,
                account.cFTP,
                plan, race
                ) if 'content' not in workout_config else Note(workout_config) for workout_config in workout_configs]

        notes = [w for w in combined if isinstance(w, Note)]
        workouts = [w for w in combined if isinstance(w, Workout)]

        return workouts, notes, plan
    except Exception:
        return [], [], ''
