import glob
import account
import os
from datetime import date
from garminworkouts.config import configreader
from garminworkouts.models.workout import Workout
from garminworkouts.models.note import Note


def settings(args, defaultPlanning=None) -> tuple[list[Workout], list[Note], str]:
    try:
        if defaultPlanning:
            planning = defaultPlanning
        else:
            planning: dict = configreader.read_config(os.path.join('.', 'events', 'planning', 'planning.yaml'))
    except FileNotFoundError:
        print('Planning config not found')
        planning = {}

    args.trainingplan = ''.join(args.trainingplan) if isinstance(args.trainingplan, tuple) else args.trainingplan

    if args.trainingplan in planning:
        workout_files: list = glob.glob(planning[args.trainingplan].get('workouts'))
        race: date = date.today()
        plan = args.trainingplan

        if 'year' in planning[args.trainingplan]:
            race = date(
                planning[args.trainingplan].get('year'),
                planning[args.trainingplan].get('month'),
                planning[args.trainingplan].get('day')
                )
    elif '.yaml' in args.trainingplan:
        workout_files = glob.glob(args.trainingplan)
        plan: str = ''
        race = date.today()
    else:
        print(f'{args.trainingplan} not found in planning, please check "planning.yaml"')
        return [], [], ''

    try:
        target: dict = configreader.read_config(r'target.yaml')
        workout_configs: list[dict] = [configreader.read_config(workout_file) for workout_file in workout_files]
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
                plan,
                race)
            if 'content' not in workout_config else Note(workout_config) for workout_config in workout_configs]

        notes: list[Note] = [w for w in combined if isinstance(w, Note)]
        workouts: list[Workout] = [w for w in combined if isinstance(w, Workout)]
        return workouts, notes, plan

    except FileNotFoundError as e:
        print(f"Error reading config file: {e}")
        return [], [], ''
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], [], ''
