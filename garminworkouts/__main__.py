#!/usr/bin/env python3

import argparse
import glob
import logging
import os

from garminworkouts.config import configreader
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.workout import Workout
from garminworkouts.utils.validators import writeable_dir
from garminworkouts.utils.envdefault import EnvDefault


def command_import(args):
    workout_files = glob.glob(args.workout)

    workout_configs = [configreader.read_config(workout_file) for workout_file in workout_files]
    workouts = [Workout(workout_config, args.ftp, args.target_power_diff) for workout_config in workout_configs]

    with _garmin_client(args) as connection:
        existing_workouts_by_name = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for workout in workouts:
            workout_name = workout.get_workout_name()
            existing_workout = existing_workouts_by_name.get(workout_name)

            if existing_workout:
                workout_id = Workout.extract_workout_id(existing_workout)
                workout_owner_id = Workout.extract_workout_owner_id(existing_workout)
                payload = workout.create_workout(workout_id, workout_owner_id)
                logging.info("Updating workout '%s'", workout_name)
                connection.update_workout(workout_id, payload)
            else:
                payload = workout.create_workout()
                logging.info("Creating workout '%s'", workout_name)
                connection.save_workout(payload)


def command_export(args):
    with _garmin_client(args) as connection:
        for workout in connection.list_workouts():
            workout_id = Workout.extract_workout_id(workout)
            workout_name = Workout.extract_workout_name(workout)
            file = os.path.join(args.directory, str(workout_id)) + ".fit"
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            connection.download_workout(workout_id, file)


def command_list(args):
    with _garmin_client(args) as connection:
        for workout in connection.list_workouts():
            Workout.print_workout_summary(workout)


def command_schedule(args):
    with _garmin_client(args) as connection:
        workout_id = args.workout_id
        date = args.date
        connection.schedule_workout(workout_id, date)


def command_get(args):
    with _garmin_client(args) as connection:
        workout = connection.get_workout(args.id)
        Workout.print_workout_json(workout)


def command_delete(args):
    with _garmin_client(args) as connection:
        logging.info("Deleting workout '%s'", args.id)
        connection.delete_workout(args.id)


def _garmin_client(args):
    return GarminClient(
        connect_url=args.connect_url,
        sso_url=args.sso_url,
        username=args.username,
        password=args.password,
        cookie_jar=args.cookie_jar
    )


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Manage Garmin Connect workout(s)")
    parser.add_argument("--username", "-u", action=EnvDefault, env_var="GARMIN_USERNAME",
                        required=True, help="Garmin Connect account username")
    parser.add_argument("--password", "-p", action=EnvDefault, env_var="GARMIN_PASSWORD",
                        required=True, help="Garmin Connect account password")
    parser.add_argument("--cookie-jar", default=".garmin-cookies.txt", help="Filename with authentication cookies")
    parser.add_argument("--connect-url", default="https://connect.garmin.com", help="Garmin Connect url")
    parser.add_argument("--sso-url", default="https://sso.garmin.com", help="Garmin SSO url")
    parser.add_argument("--debug", action='store_true', help="Enables more detailed messages")

    subparsers = parser.add_subparsers(title="Commands")

    parser_import = subparsers.add_parser("import", description="Import workout(s) from file(s) into Garmin Connect")
    parser_import.add_argument("workout",
                               help="File(s) with workout(s) to import, "
                                    "wildcards are supported e.g: sample_workouts/*.yaml")
    parser_import.add_argument("--ftp", required=True, type=int,
                               help="FTP to calculate absolute target power from relative value")
    parser_import.add_argument("--target-power-diff", default=0.05, type=float,
                               help="Percent of target power to calculate final target power range")
    parser_import.set_defaults(func=command_import)

    parser_export = subparsers.add_parser("export",
                                          description="Export all workouts from Garmin Connect and save into directory")
    parser_export.add_argument("directory", type=writeable_dir,
                               help="Destination directory where workout(s) will be exported")
    parser_export.set_defaults(func=command_export)

    parser_list = subparsers.add_parser("list", description="List all workouts")
    parser_list.set_defaults(func=command_list)

    parser_schedule = subparsers.add_parser("schedule", description="Schedule a workouts")
    parser_schedule.add_argument("--workout_id", "-w", required=True, help="Workout id to schedule")
    parser_schedule.add_argument("--date", "-d", required=True, help="Date to which schedule the workout")
    parser_schedule.set_defaults(func=command_schedule)

    parser_get = subparsers.add_parser("get", description="Get workout")
    parser_get.add_argument("--id", required=True, help="Workout id, use list command to get workouts identifiers")
    parser_get.set_defaults(func=command_get)

    parser_delete = subparsers.add_parser("delete", description="Delete workout")
    parser_delete.add_argument("--id", required=True, help="Workout id, use list command to get workouts identifiers")
    parser_delete.set_defaults(func=command_delete)

    args = parser.parse_args()

    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
