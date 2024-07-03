#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from datetime import date, timedelta
from garminworkouts.config import configreader
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.settings import planning_workout_files, settings
from garminworkouts.models.workout import Workout
from garminworkouts.models.event import Event
from garminworkouts.utils.validators import writeable_dir
import account


def command_activity_list() -> None:
    with _garmin_client() as connection:
        connection.activity_list()


def command_trainingplan_reset(args) -> None:
    with _garmin_client() as connection:
        connection.trainingplan_reset(args)


def command_trainingplan_import(args) -> None:
    workouts, notes, plan = settings(args)

    with _garmin_client() as connection:
        ue, ce, ne = connection.get_calendar(date=date.today(), days=7)

        connection.update_workouts(ue, workouts, plan)
        connection.update_notes(ne, notes, plan)


def command_event_import(args) -> None:
    event_files, _, _ = planning_workout_files(args)
    event_configs: list[dict] = [configreader.read_config(event_file) for event_file in event_files]
    events: list = [Event(event_config) for event_config in event_configs]

    with _garmin_client() as connection:
        connection.update_events(events)
        command_trainingplan_import(args)


def command_find_events(args) -> None:
    with _garmin_client() as connection:
        connection._find_events()


def command_trainingplan_metrics(args) -> None:
    workouts, *_ = settings(args)

    mileage: list[float] = [float(0) for _ in range(24, -11, -1)]
    duration: list[timedelta] = [timedelta(seconds=0) for i in range(24, -11, -1)]
    tss: list[float] = [float(0) for _ in range(24, -11, -1)]

    day_min: date | None = None
    day_max: date | None = None

    for workout in workouts:
        workout_name: str = workout.get_workout_name()
        day_d, week, _ = workout.get_workout_date()
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
        tss[week] = tss[week] + workout.tss * workout.duration.seconds

        print(workout_name, round(workout.mileage, 2), round(workout.tss, 2))

    logging.info('From ' + str(day_min) + ' to ' + str(day_max))
    for i in range(24, -11, -1):
        if mileage[i] > float(0):
            logging.info('Week ' + str(i) + ': '
                         + str(round(mileage[i], 2)) + ' km - '
                         + 'Duration: ' + str(duration[i]) + ' - '
                         + 'rTSS: ' + str(round(tss[i]/duration[i].seconds, 2)))


def command_workout_export(args) -> None:
    with _garmin_client() as connection:
        connection.workout_export(args=args)


def command_workout_export_yaml(args) -> None:
    with _garmin_client() as connection:
        connection.workout_export_yaml()


def command_workout_list(args) -> None:
    with _garmin_client() as connection:
        connection.workout_list()


def command_event_list(args) -> None:
    with _garmin_client() as connection:
        connection.event_list()


def command_trainingplan_list() -> None:
    with _garmin_client() as connection:
        connection.trainingplan_list()


def command_challenge_list() -> None:
    with _garmin_client() as connection:
        connection.list_challenge()


def command_workout_schedule(args) -> None:
    with _garmin_client() as connection:
        connection.schedule_workout(args.workout_id, args.date)


def command_workout_get(args) -> None:
    with _garmin_client() as connection:
        Workout.print_workout_json(connection.get_workout(args.id))


def command_event_get(args) -> None:
    with _garmin_client() as connection:
        Event.print_event_json(connection.get_event(args.id))


def command_workout_delete(args) -> None:
    with _garmin_client() as connection:
        connection.delete_workout(args.id)


def command_user_zones() -> None:
    with _garmin_client() as connection:
        connection.user_zones()


def command_update_types() -> None:
    with _garmin_client() as connection:
        connection.get_types()


def updateGarmin() -> None:
    with _garmin_client() as connection:
        connection.updateGarmin()


def _garmin_client() -> GarminClient:
    return GarminClient(
        email=account.EMAIL,
        password=account.PASSWORD)


def main() -> None:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Manage Garmin Connect workout(s)')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Enables more detailed messages')

    subparsers: argparse._SubParsersAction[argparse.ArgumentParser] = parser.add_subparsers(title='Commands')

    parser_import = subparsers.add_parser('trainingplan-import',
                                          description='Import workout(s) from file(s) into Garmin Connect ')
    parser_import.add_argument('trainingplan',
                               help='File(s) with workout(s) to import, '
                                    'wildcards are supported e.g: sample_workouts/*.yaml '
                                    'Additionally internal trainingplan IDs (defined in planning.yaml) may be used')
    parser_import.set_defaults(func=command_trainingplan_import)

    parser_import = subparsers.add_parser('trainingplan-reset',
                                          description='Reset workout(s) from file(s) into Garmin Connect')
    parser_import.add_argument('trainingplan',
                               help='File(s) with workout(s) to reset, '
                                    'wildcards are supported e.g: sample_workouts/*.yaml '
                                    'Additionally internal trainingplan IDs (defined in planning.yaml) may be used')
    parser_import.set_defaults(func=command_trainingplan_reset)

    parser_import = subparsers.add_parser('trainingplan-metrics',
                                          description='Get workout(s) metrics from file(s)')
    parser_import.add_argument('trainingplan',
                               help='File(s) with workout(s) to import, '
                                    'wildcards are supported e.g: sample_workouts/*.yaml '
                                    'Additionally internal trainingplan IDs (defined in planning.yaml) may be used')
    parser_import.set_defaults(func=command_trainingplan_metrics)

    parser_list = subparsers.add_parser('trainingplan-list', description='List all Garmin trainingplans')
    parser_list.set_defaults(func=command_trainingplan_list)

    parser_import: argparse.ArgumentParser = subparsers.add_parser('event-import', description='Import event(s) from \
        file(s) into Garmin Connect')
    parser_import.add_argument('trainingplan',
                               help='File(s) with event(s) to import, '
                                    'wildcards are supported e.g: events/*.yaml')
    parser_import.set_defaults(func=command_event_import)

    parser_get = subparsers.add_parser('event-get',
                                       description='Get event')
    parser_get.add_argument('--id',
                            required=True,
                            help='Event id, use list command to get event identifiers')
    parser_get.set_defaults(func=command_event_get)

    parser_list: argparse.ArgumentParser = subparsers.add_parser('event-list', description='List all events')
    parser_list.set_defaults(func=command_event_list)

    parser_get: argparse.ArgumentParser = subparsers.add_parser('workout-get', description='Get workout')
    parser_get.add_argument('--id',
                            required=True,
                            help="Workout id, use list command to get workouts' identifiers")
    parser_get.set_defaults(func=command_workout_get)

    parser_delete = subparsers.add_parser('workout-delete',
                                          description='Delete workout')
    parser_delete.add_argument('--id',
                               required=True,
                               help='Workout id, use list command to get workouts identifiers')
    parser_delete.set_defaults(func=command_workout_delete)

    parser_schedule: argparse.ArgumentParser = subparsers.add_parser('workout-schedule', description='Schedule a \
        workout')
    parser_schedule.add_argument('--workout_id',
                                 '-w',
                                 required=True,
                                 help='Workout id to schedule')
    parser_schedule.add_argument('--date',
                                 '-d',
                                 required=True,
                                 help='Date to which schedule the workout')
    parser_schedule.set_defaults(func=command_workout_schedule)

    parser_export: argparse.ArgumentParser = subparsers.add_parser('workout-export', description='Export all workouts \
        from Garmin Connect and save them into a directory')
    parser_export.add_argument('directory',
                               type=writeable_dir,
                               help='Destination directory where workout(s) will be exported')
    parser_export.set_defaults(func=command_workout_export)

    parser_export = subparsers.add_parser('workout-export-yaml',
                                          description='Export all workouts from Garmin Connect\
                                              and save them into a directory')
    parser_export.set_defaults(func=command_workout_export_yaml)

    parser_list = subparsers.add_parser('workout-list', description='List all workouts')
    parser_list.set_defaults(func=command_workout_list)

    parser_import = subparsers.add_parser('user-zones',
                                          description='Get training zones')
    parser_import.set_defaults(func=command_user_zones)

    parser_delete = subparsers.add_parser('update-types',
                                          description='Update types')
    parser_delete.set_defaults(func=command_update_types)

    parser_delete = subparsers.add_parser('activity-list',
                                          description='Activity list')
    parser_delete.set_defaults(func=command_activity_list)

    parser_delete = subparsers.add_parser('find-events',
                                          description='Find events')
    parser_delete.set_defaults(func=command_find_events)

    parser_delete: argparse.ArgumentParser = subparsers.add_parser('challenge-signup', description='Challenge sign up')
    parser_delete.set_defaults(func=command_challenge_list)

    parser_delete = subparsers.add_parser('garmin-update', description='Garmin version update')
    parser_delete.set_defaults(func=updateGarmin)

    args: argparse.Namespace = parser.parse_args()

    logging_level: int = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level,
                        handlers=[
                            logging.FileHandler(debug_file),
                            logging.StreamHandler(sys.stdout)
                        ])

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_usage()


debug_file = './debug.log'

if __name__ == '__main__':
    if os.path.exists(debug_file):
        os.remove(debug_file)
    main()
