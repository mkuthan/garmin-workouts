#!/usr/bin/env python3

import argparse
import glob
import logging
import os
from datetime import date, timedelta

from garminworkouts.config import configreader
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.settings import settings
from garminworkouts.models.workout import Workout
from garminworkouts.models.event import Event
from garminworkouts.models.trainingplan import TrainingPlan
from garminworkouts.models.extraction import export_yaml
from garminworkouts.utils.validators import writeable_dir
from garminworkouts.models.fields import _WORKOUT_ID, _ID

import account


def command_trainingplan_reset(args):
    workouts, plan = settings(args)

    with _garmin_client(args) as connection:
        existing_workouts_by_name = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for workout in workouts:
            workout_name = workout.get_workout_name()
            existing_workout = existing_workouts_by_name.get(workout_name)

            if existing_workout:
                workout_id = Workout.extract_workout_id(existing_workout)
                logging.info("Deleting workout '%s'", workout_name)
                connection.delete_workout(workout_id)


def command_workout_import(args):
    workouts, plan = settings(args)

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
                connection.get_calendar(date.today())


def command_event_import(args):
    try:
        planning = configreader.read_config(r'planning.yaml')
        event_files = glob.glob(planning[args.workout]['workouts'])
    except KeyError:
        print(args.workout + ' not found in planning, please check "planning.yaml"')
        event_files = glob.glob(args.workout)

    event_configs = [configreader.read_config(event_file) for event_file in event_files]
    events = [Event(event_config) for event_config in event_configs]

    with _garmin_client(args) as connection:
        existing_events_by_name = {Event.extract_event_name(w): w for w in connection.list_events()}
        existing_workouts_by_name = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for event in events:
            existing_event = existing_events_by_name.get(event.name)
            existing_workout = existing_workouts_by_name.get(event.name)
            workout_id = Workout.extract_workout_id(existing_workout) if existing_workout else None

            if existing_event:
                event_id = Event.extract_event_id(existing_event)
                payload = event.create_event(event_id, workout_id)
                logging.info("Updating event '%s'", event.name)
                connection.update_event(event_id, payload)
            else:
                payload = event.create_event(workout_id=workout_id)
                logging.info("Creating event '%s'", event.name)
                connection.save_event(payload)

        command_workout_import(args)


def command_trainingplan_metrics(args):
    workouts, plan = settings(args)

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


def command_workout_export(args):
    with _garmin_client(args) as connection:
        for workout in connection.list_workouts():
            workout_id = Workout.extract_workout_id(workout)
            workout_name = Workout.extract_workout_name(workout)
            file = os.path.join(args.directory, str(workout_id)) + ".fit"
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            connection.download_workout(workout_id, file)


def command_workout_export_yaml(args):
    with _garmin_client(args) as connection:
        for workout in connection.external_workouts(account.locale):
            code = workout['workoutSourceId']
            workout = connection.get_external_workout(code, account.locale)
            workout[_WORKOUT_ID] = code

            workout_id = Workout.extract_workout_id(workout)
            workout_name = Workout.extract_workout_name(workout)
            newpath = os.path.join('.\\workouts')
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            file = os.path.join(newpath, str(workout_id)) + ".yaml"
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            export_yaml(workout, file)

        for tp in connection.list_trainingplans(account.locale):
            tp = TrainingPlan.export_trainingplan(tp)
            tp_type = tp['type']
            tp_subtype = tp['subtype']
            tp_level = tp['level']
            tp_version = tp['version']

            tp = connection.schedule_training_plan(tp[_ID], str(date.today()))

            for w in connection.get_training_plan(TrainingPlan.export_trainingplan(tp)[_ID], account.locale):
                if w['taskWorkout']:
                    week = w['weekId']
                    day = w['dayOfWeekId']
                    workout_id = w['taskWorkout']['workoutId']
                    workout_name = f'R{week}_{day}'
                    workout = connection.get_workout(workout_id)

                    newpath = os.path.join('.\\trainingplans', tp_type, tp_subtype, tp_level, tp_version)
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)

                    file = os.path.join(newpath, workout_name) + ".yaml"
                    logging.info("Exporting workout '%s' into '%s'", workout_name, file)
                    export_yaml(workout, file)

            connection.delete_training_plan(tp['trainingPlanId'])

        for workout in connection.list_workouts():
            workout_id = Workout.extract_workout_id(workout)
            workout_name = Workout.extract_workout_name(workout)
            file = os.path.join('.\\exported', str(workout_id)) + ".yaml"
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            connection.download_workout_yaml(workout_id, file)


def command_workout_list(args):
    with _garmin_client(args) as connection:
        for workout in connection.list_workouts():
            Workout.print_workout_summary(workout)


def command_event_list(args):
    with _garmin_client(args) as connection:
        for event in connection.list_events():
            Event.print_event_summary(event)


def command_trainingplan_list(args):
    with _garmin_client(args) as connection:
        for tp in connection.list_trainingplans(account.locale):
            TrainingPlan.print_trainingplan_summary(tp)


def command_workout_schedule(args):
    with _garmin_client(args) as connection:
        connection.schedule_workout(args.workout_id, args.date)


def command_workout_get(args):
    with _garmin_client(args) as connection:
        Workout.print_workout_json(connection.get_workout(args.id))


def command_event_get(args):
    with _garmin_client(args) as connection:
        Event.print_event_json(connection.get_event(args.id))


def command_workout_delete(args):
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


def command_user_zones(args):
    Workout([],
            [],
            account.vV02,
            account.fmin,
            account.fmax,
            account.rFTP,
            account.cFTP,
            str(''),
            date.today()
            ).zones()


def command_update_types(args):
    with _garmin_client(args) as connection:
        connection.get_types()


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

    parser_import = subparsers.add_parser("trainingplan-reset",
                                          description="Reset workout(s) from file(s) into Garmin Connect")
    parser_import.add_argument("workout",
                               help="File(s) with workout(s) to reset, "
                                    "wildcards are supported e.g: sample_workouts/*.yaml")
    parser_import.set_defaults(func=command_trainingplan_reset)

    parser_import = subparsers.add_parser("import-workout",
                                          description="Import workout(s) from file(s) into Garmin Connect")
    parser_import.add_argument("workout",
                               help="File(s) with workout(s) to import, "
                                    "wildcards are supported e.g: sample_workouts/*.yaml")
    parser_import.set_defaults(func=command_workout_import)

    parser_import = subparsers.add_parser("import-event",
                                          description="Import event(s) from file(s) into Garmin Connect")
    parser_import.add_argument("workout",
                               help="File(s) with event(s) to import, "
                                    "wildcards are supported e.g: events/*.yaml")
    parser_import.set_defaults(func=command_event_import)

    parser_import = subparsers.add_parser("trainingplan-metrics",
                                          description="Get workout(s) metrics from file(s)")
    parser_import.add_argument("workout",
                               help="File(s) with workout(s) to import, "
                                    "wildcards are supported e.g: sample_workouts/*.yaml")
    parser_import.set_defaults(func=command_trainingplan_metrics)

    parser_import = subparsers.add_parser("zones",
                                          description="Get training zones")
    parser_import.set_defaults(func=command_user_zones)

    parser_export = subparsers.add_parser("export-workout",
                                          description="Export all workouts from Garmin Connect\
                                              and save them into a directory")
    parser_export.add_argument("directory",
                               type=writeable_dir,
                               help="Destination directory where workout(s) will be exported")
    parser_export.set_defaults(func=command_workout_export)

    parser_export = subparsers.add_parser("export-yaml",
                                          description="Export all workouts from Garmin Connect\
                                              and save them into a directory")
    parser_export.set_defaults(func=command_workout_export_yaml)

    parser_list = subparsers.add_parser("trainingplan-list", description="List all workouts")
    parser_list.set_defaults(func=command_trainingplan_list)

    parser_list = subparsers.add_parser("workout-list", description="List all workouts")
    parser_list.set_defaults(func=command_workout_list)

    parser_list = subparsers.add_parser("event-list", description="List all events")
    parser_list.set_defaults(func=command_event_list)

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
    parser_schedule.set_defaults(func=command_workout_schedule)

    parser_get = subparsers.add_parser("get-workout",
                                       description="Get workout")
    parser_get.add_argument("--id",
                            required=True,
                            help="Workout id, use list command to get workouts identifiers")
    parser_get.set_defaults(func=command_workout_get)

    parser_get = subparsers.add_parser("get-event",
                                       description="Get event")
    parser_get.add_argument("--id",
                            required=True,
                            help="Event id, use list command to get event identifiers")
    parser_get.set_defaults(func=command_event_get)

    parser_delete = subparsers.add_parser("delete-workout",
                                          description="Delete workout")
    parser_delete.add_argument("--id",
                               required=True,
                               help="Workout id, use list command to get workouts identifiers")
    parser_delete.set_defaults(func=command_workout_delete)

    parser_delete = subparsers.add_parser("update-types",
                                          description="Update types")
    parser_delete.set_defaults(func=command_update_types)

    args = parser.parse_args()

    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level)

    args.func(args)


if __name__ == "__main__":
    main()
