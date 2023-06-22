#!/usr/bin/env python3

import argparse
import glob
import logging
import os
from datetime import date, timedelta

from garminworkouts.config import configreader
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.running_workout import Workout, Event
from garminworkouts.utils.validators import writeable_dir

import account


def command_reset(args):
    workouts, plan = setting(args)

    with _garmin_client(args) as connection:
        existing_workouts_by_name = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for workout in workouts:
            workout_name = workout.get_workout_name()
            existing_workout = existing_workouts_by_name.get(workout_name)

            if existing_workout:
                workout_id = Workout.extract_workout_id(existing_workout)
                logging.info("Deleting workout '%s'", workout_name)
                connection.delete_workout(workout_id)


def command_import(args):
    workouts, plan = setting(args)

    with _garmin_client(args) as connection:
        existing_workouts_by_name = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for workout in workouts:
            workout_name = workout.get_workout_name()
            day_d, week, day = workout.get_workout_date()

            if day_d >= date.today():
                existing_workout = existing_workouts_by_name.get(workout_name)
                if existing_workout:
                    workout_id = Workout.extract_workout_id(existing_workout)
                    description = Workout.extract_workout_description(existing_workout)
                    if description and (plan in description) and (day_d <= date.today() + timedelta(weeks=2)):
                        workout_owner_id = Workout.extract_workout_owner_id(existing_workout)
                        payload = workout.create_workout(workout_id, workout_owner_id)
                        logging.info("Updating workout '%s'", workout_name)
                        connection.update_workout(workout_id, payload)
                else:
                    payload = workout.create_workout()
                    logging.info("Creating workout '%s'", workout_name)
                    connection.save_workout(payload)

                    existing_workouts_by_name = {Workout.extract_workout_name(w):
                                                 w for w in connection.list_workouts()}
                    existing_workout = existing_workouts_by_name.get(workout_name)
                    workout_id = Workout.extract_workout_id(existing_workout)
                    connection.schedule_workout(workout_id, day_d.isoformat())
            else:
                logging.info("Deleting workout '%s'", workout_name)
                connection.get_calendar(date.today())


def command_import_event(args):
    try:
        planning = configreader.read_config(r'planning.yaml')
        event_files = glob.glob(planning[args.event]['workouts'])
    except KeyError:
        print(args.workout + ' not found in planning, please check "planning.yaml"')
        event_files = glob.glob(args.event)

    event_configs = [configreader.read_config(event_file) for event_file in event_files]
    events = [Event(event_config) for event_config in event_configs]

    with _garmin_client(args) as connection:
        existing_events_by_name = {Event.extract_event_name(w): w for w in connection.list_events()}
        existing_workouts_by_name = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for event in events:
            event_name = event.name
            existing_event = existing_events_by_name.get(event_name)

            existing_workout = existing_workouts_by_name.get(event_name)
            workout_id = Workout.extract_workout_id(existing_workout) if existing_workout else None

            if existing_event:
                event_id = Event.extract_event_id(existing_event)
                payload = event.create_event(event_id, workout_id)
                logging.info("Updating event '%s'", event_name)
                connection.update_event(event_id, payload)
            else:
                payload = event.create_event(workout_id=workout_id)
                logging.info("Creating event '%s'", event_name)
                connection.save_event(payload)


def command_metrics(args):
    workouts, plan = setting(args)

    mileage = [float(0) for i in range(24, -11, -1)]
    duration = [timedelta(seconds=0) for i in range(24, -11, -1)]
    tss = [float(0) for i in range(24, -11, -1)]

    for workout in workouts:
        workout_name = workout.get_workout_name()
        day_d, week, day = workout.get_workout_date()

        mileage[week] = mileage[week] + workout.mileage
        duration[week] = duration[week] + workout.duration
        tss[week] = tss[week] + workout.tss

        print(workout_name, round(workout.mileage, 2), round(workout.tss, 2))

    for i in range(24, -11, -1):
        if mileage[i] > float(0):
            print('Week ' + str(i) + ': '
                  + str(round(mileage[i], 2)) + ' km - '
                  + 'Duration: ' + str(duration[i]) + ' - '
                  + 'rTSS: ' + str(tss[i]))


def command_export(args):
    with _garmin_client(args) as connection:
        for workout in connection.list_workouts():
            workout_id = Workout.extract_workout_id(workout)
            workout_name = Workout.extract_workout_name(workout)
            file = os.path.join(args.directory, str(workout_id)) + ".fit"
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            connection.download_workout(workout_id, file)


def command_export_yaml(args):
    with _garmin_client(args) as connection:
        for workout in connection.list_workouts():
            workout_id = Workout.extract_workout_id(workout)
            workout_name = Workout.extract_workout_name(workout)
            file = os.path.join(args.directory, str(workout_id)) + ".yaml"
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            connection.download_workout_yaml(workout_id, file)


def command_list(args):
    with _garmin_client(args) as connection:
        for workout in connection.list_workouts():
            Workout.print_workout_summary(workout)


def command_list_events(args):
    with _garmin_client(args) as connection:
        for event in connection.list_events():
            Event.print_event_summary(event)


def command_schedule(args):
    with _garmin_client(args) as connection:
        connection.schedule_workout(args.workout_id, args.date)


def command_get(args):
    with _garmin_client(args) as connection:
        workout = connection.get_workout(args.id)
        Workout.print_workout_json(workout)


def command_get_event(args):
    with _garmin_client(args) as connection:
        event = connection.get_event(args.id)
        Event.print_event_json(event)


def command_delete(args):
    with _garmin_client(args) as connection:
        logging.info("Deleting workout '%s'", args.id)
        connection.delete_workout(args.id)


def _garmin_client(args):
    return GarminClient(
        connect_url=args.connect_url,
        sso_url=args.sso_url,
        username=account.USERNAME,
        password=account.PASSWORD,
        cookie_jar=args.cookie_jar
    )


def setting(args):
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
    target = configreader.read_config(r'pace.yaml')
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


def command_zones(args):
    Workout([],
            [],
            account.vV02,
            account.fmin,
            account.fmax,
            account.rFTP,
            account.cFTP,
            str(''),
            date(0, 1, 1)
            ).zones()


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Manage Garmin Connect workout(s)")
    parser.add_argument("--cookie-jar",
                        default=".garmin-cookies.txt",
                        help="Filename with authentication cookies")
    parser.add_argument("--connect-url",
                        default="https://connect.garmin.com",
                        help="Garmin Connect url")
    parser.add_argument("--sso-url",
                        default="https://sso.garmin.com",
                        help="Garmin SSO url")
    parser.add_argument("--debug",
                        action='store_true',
                        help="Enables more detailed messages")

    subparsers = parser.add_subparsers(title="Commands")

    parser_import = subparsers.add_parser("reset",
                                          description="Reset workout(s) from file(s) into Garmin Connect")
    parser_import.add_argument("workout",
                               help="File(s) with workout(s) to reset, "
                                    "wildcards are supported e.g: sample_workouts/*.yaml")
    parser_import.set_defaults(func=command_reset)

    parser_import = subparsers.add_parser("import",
                                          description="Import workout(s) from file(s) into Garmin Connect")
    parser_import.add_argument("workout",
                               help="File(s) with workout(s) to import, "
                                    "wildcards are supported e.g: sample_workouts/*.yaml")
    parser_import.set_defaults(func=command_import)

    parser_import = subparsers.add_parser("event",
                                          description="Import event(s) from file(s) into Garmin Connect")
    parser_import.add_argument("event",
                               help="File(s) with event(s) to import, "
                                    "wildcards are supported e.g: events/*.yaml")
    parser_import.set_defaults(func=command_import_event)

    parser_import = subparsers.add_parser("metrics",
                                          description="Get workout(s) metrics from file(s)")
    parser_import.add_argument("workout",
                               help="File(s) with workout(s) to import, "
                                    "wildcards are supported e.g: sample_workouts/*.yaml")
    parser_import.set_defaults(func=command_metrics)

    parser_import = subparsers.add_parser("zones",
                                          description="Get training zones")
    parser_import.set_defaults(func=command_zones)

    parser_export = subparsers.add_parser("export",
                                          description="Export all workouts from Garmin Connect and save into directory")
    parser_export.add_argument("directory",
                               type=writeable_dir,
                               help="Destination directory where workout(s) will be exported")
    parser_export.set_defaults(func=command_export)

    parser_export = subparsers.add_parser("export-yaml",
                                          description="Export all workouts from Garmin Connect and save into directory")
    parser_export.add_argument("directory", type=writeable_dir,
                               help="Destination directory where workout(s) will be exported")
    parser_export.set_defaults(func=command_export_yaml)

    parser_list = subparsers.add_parser("list", description="List all workouts")
    parser_list.set_defaults(func=command_list)

    parser_list = subparsers.add_parser("event-list", description="List all events")
    parser_list.set_defaults(func=command_list_events)

    parser_schedule = subparsers.add_parser("schedule",
                                            description="Schedule a workouts")
    parser_schedule.add_argument("--workout_id",
                                 "-w",
                                 required=True,
                                 help="Workout id to schedule")
    parser_schedule.add_argument("--date",
                                 "-d",
                                 required=True,
                                 help="Date to which schedule the workout")
    parser_schedule.set_defaults(func=command_schedule)

    parser_get = subparsers.add_parser("get",
                                       description="Get workout")
    parser_get.add_argument("--id",
                            required=True,
                            help="Workout id, use list command to get workouts identifiers")
    parser_get.set_defaults(func=command_get)

    parser_get = subparsers.add_parser("get-event",
                                       description="Get event")
    parser_get.add_argument("--id",
                            required=True,
                            help="Event id, use list command to get event identifiers")
    parser_get.set_defaults(func=command_get_event)

    parser_delete = subparsers.add_parser("delete",
                                          description="Delete workout")
    parser_delete.add_argument("--id",
                               required=True,
                               help="Workout id, use list command to get workouts identifiers")
    parser_delete.set_defaults(func=command_delete)

    args = parser.parse_args()

    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level)

    args.func(args)


if __name__ == "__main__":
    main()
