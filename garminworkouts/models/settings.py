from datetime import date
from typing import List, Tuple, Union, Any
import glob
import os
from garminworkouts.config import configreader
from garminworkouts.models.workout import Workout
from garminworkouts.models.note import Note
import account
import logging


def settings(args, defaultPlanning=None) -> Tuple[List[Workout], List[Note], str]:
    workout_files, race, plan = planning_workout_files(args, defaultPlanning)

    try:
        target: dict[Any, Any] = configreader.read_config(r'target.yaml')
        workout_configs: list[dict[Any, Any]] = [configreader.read_config(
            workout_file) for workout_file in workout_files]
        combined: List[Workout | Note] = [
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

        notes: List[Note] = [w for w in combined if isinstance(w, Note)]
        workouts: List[Workout] = [w for w in combined if isinstance(w, Workout)]
        return workouts, notes, plan

    except FileNotFoundError as e:
        print(f"Error reading config file: {e}")
        return [], [], ''


def planning_workout_files(args, defaultPlanning: dict | None = None):
    try:
        if defaultPlanning:
            planning: Any = defaultPlanning
        else:
            planning = configreader.read_config(os.path.join('.', 'events', 'planning', 'planning.yaml'))
    except FileNotFoundError:
        logging.error('Planning config not found')
        planning = {}

    args.trainingplan = ''.join(args.trainingplan) if isinstance(args.trainingplan, tuple) else args.trainingplan

    if args.trainingplan in planning:
        if isinstance(planning[args.trainingplan].get('workouts'), list):
            workout_files: list[dict | str] = []
            for files in planning[args.trainingplan].get('workouts'):
                workout_files.extend(glob.glob(files))
        else:
            workout_files = glob.glob(planning[args.trainingplan].get('workouts'))
        race: date = date.today()
        plan: Union[str, Any] = args.trainingplan

        if 'year' in planning[args.trainingplan]:
            race = date(
                planning[args.trainingplan].get('year'),
                planning[args.trainingplan].get('month'),
                planning[args.trainingplan].get('day')
            )
    elif '.yaml' in args.trainingplan:
        workout_files = glob.glob(args.trainingplan)
        plan = ''
        race = date.today()
    else:
        logging.error(f'{args.trainingplan} not found in planning, please check "planning.yaml"')
        workout_files = []
        plan = ''
        race = date.today()

    return workout_files, race, plan
