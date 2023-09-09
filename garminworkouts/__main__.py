#!/usr/bin/env python3

import argparse
import glob
import logging
import os
import sys
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


def command_trainingplan_reset(args) -> None:
    workouts, plan = settings(args)

    with _garmin_client(args) as connection:
        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for workout in workouts:
            workout_name: str = workout.get_workout_name()
            existing_workout: dict | None = existing_workouts_by_name.get(workout_name)

            if existing_workout:
                workout_id: str = Workout.extract_workout_id(existing_workout)
                logging.info("Deleting workout '%s'", workout_name)
                connection.delete_workout(workout_id)


def command_trainingplan_import(args, event=False) -> None:
    workouts, plan = settings(args)

    with _garmin_client(args) as connection:
        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for workout in workouts:
            workout_name: str = workout.get_workout_name()
            day_d, week, day = workout.get_workout_date()

            if day_d >= date.today():
                existing_workout: dict | None = existing_workouts_by_name.get(workout_name)
                if existing_workout:
                    description: str = Workout.extract_workout_description(existing_workout)
                    if event or ((day_d <= date.today() + timedelta(weeks=2))
                                 and description and (plan in description)):
                        workout_id: str = Workout.extract_workout_id(existing_workout)
                        workout_owner_id: str = Workout.extract_workout_owner_id(existing_workout)
                        payload: dict = workout.create_workout(workout_id, workout_owner_id)
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
        connection.get_calendar(date.today())


def command_event_import(args) -> None:
    planning: dict = configreader.read_config(os.path.join('.', 'events', 'planning', 'planning.yaml'))
    try:
        event_files: list = glob.glob(planning[args.workout]['workouts'])
    except KeyError:
        logging.error(args.workout + ' not found in planning, please check "planning.yaml"')
        event_files = glob.glob(args.workout)

    event_configs: list[dict] = [configreader.read_config(event_file) for event_file in event_files]
    events: list = [Event(event_config) for event_config in event_configs]

    with _garmin_client(args) as connection:
        existing_events_by_name: dict = {Event.extract_event_name(w): w for w in connection.list_events()}
        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for event in events:
            if event.date >= date.today():
                existing_event: dict | None = existing_events_by_name.get(event.name)
                existing_workout: dict | None = existing_workouts_by_name.get(event.name)
                workout_id: str | None = Workout.extract_workout_id(existing_workout) if existing_workout else None

                if existing_event:
                    event_id: str = Event.extract_event_id(existing_event)
                    payload: dict = event.create_event(event_id, workout_id)
                    logging.info("Updating event '%s'", event.name)
                    connection.update_event(event_id, payload)
                else:
                    payload = event.create_event(workout_id=workout_id)
                    logging.info("Creating event '%s'", event.name)
                    connection.save_event(payload)

        command_trainingplan_import(args, event=True)


def command_trainingplan_metrics(args) -> None:
    workouts, plan = settings(args)

    mileage: list[float] = [float(0) for i in range(24, -11, -1)]
    duration: list[timedelta] = [timedelta(seconds=0) for i in range(24, -11, -1)]
    tss: list[float] = [float(0) for i in range(24, -11, -1)]

    day_min: date | None = None
    day_max: date | None = None

    for workout in workouts:
        workout_name: str = workout.get_workout_name()
        day_d, week, day = workout.get_workout_date()
        if day_min is None:
            day_min = day_d
        if day_max is None:
            day_max = day_d
        if day_min > day_d:
            day_min = day_d
        if day_max < day_d:
            day_max = day_d
        mileage[week] = mileage[week] + workout.mileage
        duration[week] = duration[week] + workout.duration
        tss[week] = tss[week] + workout.tss

        print(workout_name, round(workout.mileage, 2), round(workout.tss, 2))

    logging.info('From ', str(day_min), ' to ', str(day_max))
    for i in range(24, -11, -1):
        if mileage[i] > float(0):
            logging.info('Week ' + str(i) + ': '
                         + str(round(mileage[i], 2)) + ' km - '
                         + 'Duration: ' + str(duration[i]) + ' - '
                         + 'rTSS: ' + str(tss[i]))


def command_workout_export(args) -> None:
    with _garmin_client(args) as connection:
        for workout in connection.list_workouts():
            workout_id: str = Workout.extract_workout_id(workout)
            workout_name: str = Workout.extract_workout_name(workout)
            file: str = os.path.join(args.directory, str(workout_id) + '.fit')
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            connection.download_workout(workout_id, file)


def command_workout_export_yaml(args):
    with _garmin_client(args) as connection:
        for workout in connection.external_workouts(account.locale):
            code: str = workout['workoutSourceId']
            sport: str = workout['sportTypeKey']
            difficulty: str = workout['difficulty']
            workout: dict = connection.get_external_workout(code, account.locale)
            workout[_WORKOUT_ID] = code

            workout_id: str = Workout.extract_workout_id(workout)
            workout_name: str = Workout.extract_workout_name(workout)
            newpath: str = os.path.join('.', 'workouts', sport, difficulty)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            file: str = os.path.join(newpath, str(workout_id) + '.yaml')
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            export_yaml(workout, file)

        for tp in connection.list_trainingplans(account.locale):
            tp: dict = TrainingPlan.export_trainingplan(tp)
            tp_type: str = tp['type']
            tp_subtype: str = tp['subtype']
            tp_level: str = tp['level']
            tp_version: str = tp['version']
            tp_name: str = ''.join(letter for letter in tp['name'] if letter.isalnum())

            tp = connection.schedule_training_plan(tp[_ID], str(date.today()))

            for w in connection.get_training_plan(TrainingPlan.export_trainingplan(tp)[_ID], account.locale):
                if w['taskWorkout']:
                    week: str = w['weekId']
                    day: str = w['dayOfWeekId']
                    workout_id: str = w['taskWorkout']['workoutId']
                    workout_name: str = f'R{week}_{day}'
                    workout: dict = connection.get_workout(workout_id)

                    if (tp_subtype.lower() == tp_name.lower()) or ((tp_subtype + tp_type).lower()
                                                                   == tp_name.lower()):
                        newpath: str = os.path.join('.', 'trainingplans', tp_type, tp_subtype, tp_level, tp_version)
                    else:
                        newpath: str = os.path.join('.', 'trainingplans', tp_type, tp_subtype, tp_level, tp_version,
                                                    tp_name)
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)

                    file: str = os.path.join(newpath, workout_name + ".yaml")
                    logging.info("Exporting workout '%s' into '%s'", workout_name, file)
                    export_yaml(workout, file)

            connection.delete_training_plan(tp['trainingPlanId'])

        for workout in connection.list_workouts():
            workout_id = Workout.extract_workout_id(workout)
            workout_name = Workout.extract_workout_name(workout)
            file = os.path.join('.', 'exported', str(workout_id) + '.yaml')
            logging.info("Exporting workout '%s' into '%s'", workout_name, file)
            connection.download_workout_yaml(workout_id, file)


def command_workout_list(args) -> None:
    with _garmin_client(args) as connection:
        for workout in connection.list_workouts():
            Workout.print_workout_summary(workout)


def command_event_list(args) -> None:
    with _garmin_client(args) as connection:
        for event in connection.list_events():
            Event.print_event_summary(event)


def command_trainingplan_list(args) -> None:
    with _garmin_client(args) as connection:
        for tp in connection.list_trainingplans(account.locale):
            TrainingPlan.print_trainingplan_summary(tp)


def command_workout_schedule(args) -> None:
    with _garmin_client(args) as connection:
        connection.schedule_workout(args.workout_id, args.date)


def command_workout_get(args) -> None:
    with _garmin_client(args) as connection:
        Workout.print_workout_json(connection.get_workout(args.id))


def command_event_get(args) -> None:
    with _garmin_client(args) as connection:
        Event.print_event_json(connection.get_event(args.id))


def command_workout_delete(args) -> None:
    with _garmin_client(args) as connection:
        logging.info("Deleting workout '%s'", args.id)
        connection.delete_workout(args.id)


def _garmin_client(args) -> GarminClient:
    return GarminClient(
        connect_url=args.connect_url,
        sso_url=args.sso_url,
        username=account.USERNAME,
        password=account.PASSWORD,
        cookie_jar=args.cookie_jar
    )


def command_user_zones(args) -> None:
    zones, hr_zones, data = Workout(
        [],
        [],
        account.vV02,
        account.fmin,
        account.fmax,
        account.flt,
        account.rFTP,
        account.cFTP,
        str(''),
        date.today()
        ).hr_zones()

    with _garmin_client(args) as connection:
        connection.save_hr_zones(data)

    Workout([],
            [],
            account.vV02,
            account.fmin,
            account.fmax,
            account.flt,
            account.rFTP,
            account.cFTP,
            str(''),
            date.today()
            ).zones()


def command_update_types(args) -> None:
    with _garmin_client(args) as connection:
        connection.get_types()


def main() -> None:
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

    parser_import = subparsers.add_parser("trainingplan-import",
                                          description="Import workout(s) from file(s) into Garmin Connect ")
    parser_import.add_argument("trainingplan",
                               help="File(s) with workout(s) to import, "
                                    "wildcards are supported e.g: sample_workouts/*.yaml "
                                    "Additionally internal trainingplan IDs (defined in planning.yaml) may be used")
    parser_import.set_defaults(func=command_trainingplan_import)

    parser_import = subparsers.add_parser("trainingplan-reset",
                                          description="Reset workout(s) from file(s) into Garmin Connect")
    parser_import.add_argument("trainingplan",
                               help="File(s) with workout(s) to reset, "
                                    "wildcards are supported e.g: sample_workouts/*.yaml "
                                    "Additionally internal trainingplan IDs (defined in planning.yaml) may be used")
    parser_import.set_defaults(func=command_trainingplan_reset)

    parser_import = subparsers.add_parser("trainingplan-metrics",
                                          description="Get workout(s) metrics from file(s)")
    parser_import.add_argument("trainingplan",
                               help="File(s) with workout(s) to import, "
                                    "wildcards are supported e.g: sample_workouts/*.yaml "
                                    "Additionally internal trainingplan IDs (defined in planning.yaml) may be used")
    parser_import.set_defaults(func=command_trainingplan_metrics)

    parser_list = subparsers.add_parser("trainingplan-list", description="List all Garmin trainingplans")
    parser_list.set_defaults(func=command_trainingplan_list)

    parser_import = subparsers.add_parser("event-import",
                                          description="Import event(s) from file(s) into Garmin Connect")
    parser_import.add_argument("workout",
                               help="File(s) with event(s) to import, "
                                    "wildcards are supported e.g: events/*.yaml")
    parser_import.set_defaults(func=command_event_import)

    parser_get = subparsers.add_parser("event-get",
                                       description="Get event")
    parser_get.add_argument("--id",
                            required=True,
                            help="Event id, use list command to get event identifiers")
    parser_get.set_defaults(func=command_event_get)

    parser_list = subparsers.add_parser("event-list", description="List all events")
    parser_list.set_defaults(func=command_event_list)

    parser_get = subparsers.add_parser("workout-get",
                                       description="Get workout")
    parser_get.add_argument("--id",
                            required=True,
                            help="Workout id, use list command to get workouts' identifiers")
    parser_get.set_defaults(func=command_workout_get)

    parser_delete = subparsers.add_parser("workout-delete",
                                          description="Delete workout")
    parser_delete.add_argument("--id",
                               required=True,
                               help="Workout id, use list command to get workouts identifiers")
    parser_delete.set_defaults(func=command_workout_delete)

    parser_schedule = subparsers.add_parser("workout-schedule",
                                            description="Schedule a workout")
    parser_schedule.add_argument("--workout_id",
                                 "-w",
                                 required=True,
                                 help="Workout id to schedule")
    parser_schedule.add_argument("--date",
                                 "-d",
                                 required=True,
                                 help="Date to which schedule the workout")
    parser_schedule.set_defaults(func=command_workout_schedule)

    parser_export = subparsers.add_parser("workout-export",
                                          description="Export all workouts from Garmin Connect\
                                              and save them into a directory")
    parser_export.add_argument("directory",
                               type=writeable_dir,
                               help="Destination directory where workout(s) will be exported")
    parser_export.set_defaults(func=command_workout_export)

    parser_export = subparsers.add_parser("workout-export-yaml",
                                          description="Export all workouts from Garmin Connect\
                                              and save them into a directory")
    parser_export.set_defaults(func=command_workout_export_yaml)

    parser_list = subparsers.add_parser("workout-list", description="List all workouts")
    parser_list.set_defaults(func=command_workout_list)

    parser_import = subparsers.add_parser("user-zones",
                                          description="Get training zones")
    parser_import.set_defaults(func=command_user_zones)

    parser_delete = subparsers.add_parser("update-types",
                                          description="Update types")
    parser_delete.set_defaults(func=command_update_types)

    args = parser.parse_args()

    logging_level: int = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level,
                        handlers=[
                            logging.FileHandler(debug_file),
                            logging.StreamHandler(sys.stdout)
                        ])

    args.func(args)


debug_file = './debug.log'

if __name__ == "__main__":
    if os.path.exists(debug_file):
        os.remove(debug_file)
    main()
