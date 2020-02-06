#!/usr/bin/env python3

import argparse
import glob

from config.config import read_config
from garmin.garminclient import GarminClient
from models.workout import Workout


def command_import(args):
    workout_files = glob.glob(args.workout)

    workout_configs = [read_config(workout_file) for workout_file in workout_files]
    workouts = [Workout(workout_config, args.ftp) for workout_config in workout_configs]

    with GarminClient(username=args.username, password=args.password, cookie_jar=args.cookie_jar) as connection:
        existing_workouts_by_name = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for workout in workouts:
            workout_name = workout.get_workout_name()
            existing_workout = existing_workouts_by_name.get(workout_name)

            if existing_workout:
                workout_id = Workout.extract_workout_id(existing_workout)
                workout_owner_id = Workout.extract_workout_owner_id(existing_workout)
                payload = workout.create_workout(workout_id, workout_owner_id)
                print("Updating '%s'" % workout_name, end="... ")
                connection.update_workout(workout_id, payload)
                print("done.")
            else:
                payload = workout.create_workout()
                print("Saving '%s'" % workout_name, end="... ")
                connection.save_workout(payload)
                print("done.")


def main():
    parser = argparse.ArgumentParser(description="Manage Garmin workout(s)")
    parser.add_argument("--username", "-u", required=True)
    parser.add_argument("--password", "-p", required=True)
    parser.add_argument("--cookie-jar", default=".garmin-cookies.txt")

    subparsers = parser.add_subparsers(title="Commands")

    parser_import = subparsers.add_parser("import", description="Import workout(s) from file(s)")
    parser_import.add_argument("workout")
    parser_import.add_argument("--ftp", required=True, type=int)
    parser_import.set_defaults(func=command_import)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
