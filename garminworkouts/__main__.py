#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from datetime import date
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.settings import settings
from garminworkouts.models.workout import Workout
from garminworkouts.models.event import Event
from garminworkouts.utils.validators import writeable_dir
import account


def command_trainingplan_reset(args) -> None:
    with _garmin_client() as connection:
        connection.trainingplan_reset(args)


def command_trainingplan_import(args) -> None:
    workouts, notes, _, plan = settings(args)

    with _garmin_client() as connection:
        ue, _, ne = connection.get_calendar(date=date.today(), days=7)

        connection.update_workouts(ue=ue, workouts=workouts, plan=plan)
        connection.update_notes(ne=ne, notes=notes, plan=plan)


def command_event_import(args) -> None:
    workouts, _, events, plan = settings(args)

    with _garmin_client() as connection:
        ue, _, _ = connection.get_calendar(date=date.today(), days=7)
        connection.update_events(events=events)
        connection.update_workouts(ue=ue, workouts=workouts, plan=plan)


def command_find_events(args) -> None:
    with _garmin_client() as connection:
        connection._find_events()


def command_trainingplan_metrics(args) -> None:
    workouts, *_ = settings(args)
    Workout.load_metrics(workouts=workouts)


def command_workout_export(args) -> None:
    with _garmin_client() as connection:
        connection.workout_export(args)


def command_workout_export_yaml(args) -> None:
    with _garmin_client() as connection:
        connection.external_workout_export_yaml()


def command_workout_schedule(args) -> None:
    with _garmin_client() as connection:
        connection.schedule_workout(workout_id=args.id, date=args.date)


def command_workout_get(args) -> None:
    with _garmin_client() as connection:
        Workout.print_workout_json(connection.get_workout(workout_id=args.id))


def command_event_get(args) -> None:
    with _garmin_client() as connection:
        Event.print_event_json(connection.get_event(event_id=args.id))


def command_workout_delete(args) -> None:
    with _garmin_client() as connection:
        connection.delete_workout(workout_id=args.workout_id)


def command_user_zones(args) -> None:
    with _garmin_client() as connection:
        connection.user_zones()


def command_workout_list(args) -> None:
    with _garmin_client() as connection:
        connection.workout_list()


def command_event_list(args) -> None:
    with _garmin_client() as connection:
        connection.event_list()


def command_challenge_list(args) -> None:
    with _garmin_client() as connection:
        connection.list_challenge()


def command_trainingplan_list(args) -> None:
    with _garmin_client() as connection:
        connection.trainingplan_list()


def command_activity_list(args) -> None:
    with _garmin_client() as connection:
        connection.activity_list()


def command_update_types(args) -> None:
    with _garmin_client() as connection:
        connection.get_types()


def update_garmin(args) -> None:
    with _garmin_client() as connection:
        connection.updateGarmin()


def _garmin_client() -> GarminClient:
    """
    Creates and returns a GarminClient instance using the email and password from the account module.
    Creates and returns a GarminClient instance using the email and password from the account module as a context
    manager.
    Returns:
        GarminClient: An instance of GarminClient initialized with email and password.
    Raises:
        AttributeError: If the account module does not define EMAIL and PASSWORD.
    """
    try:
        email = account.EMAIL
        password = account.PASSWORD
    except AttributeError:
        raise AttributeError("account module must define EMAIL and PASSWORD")

    return GarminClient(
        email=email,
        password=password)


def main() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Manage Garmin Connect workout(s)'
    )
    parser.add_argument('--debug',
                        action='store_true',
                        help='Enables more detailed messages')

    subparsers: argparse._SubParsersAction[argparse.ArgumentParser] = parser.add_subparsers(title='Commands')

    parser_import: argparse.ArgumentParser = subparsers.add_parser(
        'trainingplan-import',
        description='Import workout(s) from file(s) into Garmin Connect ')
    parser_import.add_argument(
        'trainingplan',
        help='File(s) with workout(s) to import, '
        'wildcards are supported e.g: sample_workouts/*.yaml '
        'Additionally internal trainingplan IDs (defined in planning.yaml) may be used')
    parser_import.set_defaults(func=command_trainingplan_import)

    parser_import = subparsers.add_parser(
        'trainingplan-reset',
        description='Reset workout(s) from file(s) into Garmin Connect')
    parser_import.add_argument(
        'trainingplan',
        help='File(s) with workout(s) to reset, '
        'wildcards are supported e.g: sample_workouts/*.yaml '
        'Additionally internal trainingplan IDs (defined in planning.yaml) may be used')
    parser_import.set_defaults(func=command_trainingplan_reset)

    parser_import = subparsers.add_parser(
        'trainingplan-metrics',
        description='Get workout(s) metrics from file(s)')
    parser_import.add_argument(
        'trainingplan',
        help='File(s) with workout(s) to import, '
        'wildcards are supported e.g: sample_workouts/*.yaml '
        'Additionally internal trainingplan IDs (defined in planning.yaml) may be used')
    parser_import.set_defaults(func=command_trainingplan_metrics)

    parser_import = subparsers.add_parser(
        'trainingplan-list', description='List all Garmin trainingplans')
    parser_import.set_defaults(func=command_trainingplan_list)

    parser_import: argparse.ArgumentParser = subparsers.add_parser(
        'event-import',
        description='Import event(s) from file(s) into Garmin Connect')
    parser_import.add_argument(
        'trainingplan',
        help='File(s) with event(s) to import, wildcards are supported e.g: events/*.yaml')
    parser_import.set_defaults(func=command_event_import)

    parser_import = subparsers.add_parser(
        'event-get',
        description='Get event')
    parser_import.add_argument(
        '--id',
        required=True,
        help='Event id, use list command to get event identifiers')
    parser_import.set_defaults(func=command_event_get)

    parser_import = subparsers.add_parser('event-list', description='List all events')
    parser_import.set_defaults(func=command_event_list)

    parser_import = subparsers.add_parser(
        'workout-get', description='Get workout')
    parser_import.add_argument(
        '--id',
        required=True,
        help="Workout id, use list command to get workouts' identifiers")
    parser_import.set_defaults(func=command_workout_get)

    parser_import: argparse.ArgumentParser = subparsers.add_parser(
        'workout-delete',
        description='Delete workout')
    parser_import.add_argument(
        '--id',
        required=True,
        help='Workout id, use list command to get workouts identifiers')
    parser_import.set_defaults(func=command_workout_delete)

    parser_import = subparsers.add_parser(
        'workout-schedule',
        description='Schedule a workout')
    parser_import.add_argument(
        '--id',
        '-w',
        required=True,
        help='Workout id to schedule')
    parser_import.add_argument(
        '--date',
        '-d',
        required=True,
        help='Date to which schedule the workout')
    parser_import.set_defaults(func=command_workout_schedule)

    parser_import = subparsers.add_parser(
        'workout-export',
        description='Export all workouts from Garmin Connect and save them into a directory')
    parser_import.add_argument(
        'directory',
        type=writeable_dir,
        help='Destination directory where workout(s) will be exported')
    parser_import.set_defaults(func=command_workout_export)

    parser_import = subparsers.add_parser(
        'workout-export-yaml',
        description='Export all workouts from Garmin Connect and save them into a directory')
    parser_import.set_defaults(func=command_workout_export_yaml)

    parser_import = subparsers.add_parser(
        'workout-list',
        description='List all workouts')
    parser_import.set_defaults(func=command_workout_list)

    parser_import = subparsers.add_parser(
        'user-zones',
        description='Get training zones')
    parser_import.set_defaults(func=command_user_zones)

    parser_import = subparsers.add_parser(
        'update-types',
        description='Update types')
    parser_import.set_defaults(func=command_update_types)

    parser_import = subparsers.add_parser(
        'activity-list',
        description='Activity list')
    parser_import.set_defaults(func=command_activity_list)

    parser_import = subparsers.add_parser(
        'find-events',
        description='Find events')
    parser_import.set_defaults(func=command_find_events)

    parser_import = subparsers.add_parser(
        'challenge-signup',
        description='Challenge sign up')
    parser_import.set_defaults(func=command_challenge_list)

    parser_import = subparsers.add_parser(
        'garmin-update',
        description='Garmin version update')
    parser_import.set_defaults(func=update_garmin)

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

if __name__ == '__main__':  # pragma: no cover
    try:
        os.remove(debug_file)
    except FileNotFoundError:
        pass
    if os.path.exists(debug_file):
        os.remove(debug_file)
    main()
