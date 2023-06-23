import glob
import account
from garminworkouts.config import configreader
from datetime import date
from garminworkouts.models.workout import Workout


def settings(args):
    workout_files = glob.glob(args.workout)
    plan = str('')
    race = account.race
    if not workout_files:
        try:
            planning = configreader.read_config(r'planning.yaml')
            workout_files = glob.glob(planning[args.workout]['workouts'])
            race = date(planning[args.workout]['year'], planning[args.workout]['month'], planning[args.workout]['day'])
            plan = args.workout
        except KeyError:
            print(args.workout + ' not found in planning, please check "planning.yaml"')

    workout_configs = [configreader.read_config(workout_file) for workout_file in workout_files]
    target = configreader.read_config(r'target.yaml')
    workouts = [Workout(workout_config,
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
