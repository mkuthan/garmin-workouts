#!/usr/bin/env python3

import argparse
import datetime
import glob
import logging
import os
import sys
from datetime import date, timedelta
import json
from garminworkouts.config import configreader
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.settings import settings
from garminworkouts.models.workout import Workout
from garminworkouts.models.event import Event
from garminworkouts.models.note import Note
from garminworkouts.models.power import Power
from garminworkouts.models.trainingplan import TrainingPlan
from garminworkouts.models.extraction import workout_export_yaml, event_export_yaml, note_export_yaml
from garminworkouts.utils.validators import writeable_dir
from garminworkouts.models.fields import _WORKOUT_ID, _ID
import account


def command_activity_list(args):
    with _garmin_client(args) as connection:
        activities = connection.get_activities_by_date(
            startdate=date.today()+datetime.timedelta(days=-7),
            enddate=date.today(),
            activitytype='running'
            )
        print(activities)


def command_trainingplan_reset(args) -> None:
    workouts, notes,  plan = settings(args)

    with _garmin_client(args) as connection:
        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}

        for workout in workouts:
            workout_name: str = workout.get_workout_name()
            existing_workout: dict | None = existing_workouts_by_name.get(workout_name)

            if existing_workout and plan in existing_workout['description']:
                workout_id: str = Workout.extract_workout_id(existing_workout)
                logging.info("Deleting workout '%s'", workout_name)
                connection.delete_workout(workout_id)


def command_trainingplan_import(args, event=False) -> None:
    workouts, notes, plan = settings(args)
    workouts_by_name: dict = {w.get_workout_name(): w for w in workouts}

    with _garmin_client(args) as connection:
        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in connection.list_workouts()}
        ue, ce = connection.get_calendar(date=date.today(), days=7)

        for wname in ue:
            existing_workout: dict | None = existing_workouts_by_name.get(
                wname) if wname in workouts_by_name else None
            if existing_workout and plan in existing_workout['description']:
                workout_id: str = Workout.extract_workout_id(existing_workout)
                workout_owner_id: str = Workout.extract_workout_owner_id(existing_workout)
                workout_author: dict = Workout.extract_workout_author(existing_workout)
                workout: Workout = workouts_by_name[wname]
                payload: dict = workout.create_workout(workout_id, workout_owner_id, workout_author)
                logging.info("Updating workout '%s'", wname)
                connection.update_workout(workout_id, payload)

        for workout in workouts:
            day_d, week, day = workout.get_workout_date()

            if day_d >= date.today() and day_d < date.today() + timedelta(weeks=2):
                workout_name: str = workout.get_workout_name()
                existing_workout: dict | None = existing_workouts_by_name.get(workout_name)
                if not existing_workout:
                    payload = workout.create_workout()
                    logging.info("Creating workout '%s'", workout_name)
                    workout_id = Workout.extract_workout_id(connection.save_workout(payload))
                    connection.schedule_workout(workout_id, day_d.isoformat())


def command_event_import(args) -> None:
    planning: dict = configreader.read_config(os.path.join('.', 'events', 'planning', 'planning.yaml'))
    try:
        event_files: list = glob.glob(planning[args.trainingplan]['workouts'])
    except KeyError:
        logging.error(args.trainingplan + ' not found in planning, please check "planning.yaml"')
        event_files = glob.glob(args.trainingplan)

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


def command_find_events(args):
    with _garmin_client(args) as connection:
        events = connection.find_events()
        for subev in events:
            for ev in subev:
                ev_a = json.loads(ev.decode('utf-8'))
                if ("administrativeArea" in ev_a) and (ev_a["administrativeArea"] is not None) and (
                     ev_a["administrativeArea"]['countryCode'] is not None):
                    newpath: str = os.path.join('.', 'exported', 'events', ev_a['eventType'],
                                                ev_a["administrativeArea"]['countryCode'])
                else:
                    newpath: str = os.path.join('.', 'exported', 'events', ev_a['eventType'])
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                file: str = os.path.join(newpath, ev_a['eventRef'] + '.yaml')
                event_export_yaml(connection.get(ev_a['detailsEndpoints'][0]['url']).json(), file)


def command_trainingplan_metrics(args) -> None:
    workouts, notes, plan = settings(args)

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
            workout_export_yaml(workout, file)

        for tp in connection.list_trainingplans(account.locale):
            tp: dict = TrainingPlan.export_trainingplan(tp)
            tp_type: str = tp['type']
            tp_subtype: str = tp['subtype']
            tp_level: str = tp['level']
            tp_version: str = tp['version']
            tp_name: str = ''.join(letter for letter in tp['name'] if letter.isalnum())

            tp = connection.schedule_training_plan(tp[_ID], str(date.today()))

            if tp_subtype == 'RunningOther':
                tp_subtype = tp_name
                tp_name = ''

            if (tp_subtype.lower() == tp_name.lower()) or ((tp_subtype + tp_type).lower() == tp_name.lower()):
                newpath: str = os.path.join('.', 'trainingplans', tp_type, 'Garmin', tp_subtype, tp_level, tp_version)
            else:
                newpath: str = os.path.join('.', 'trainingplans', tp_type, 'Garmin', tp_subtype, tp_level, tp_version,
                                            tp_name)

            for w in connection.get_training_plan(TrainingPlan.export_trainingplan(tp)[_ID], account.locale):
                week: str = w['weekId']
                day: str = w['dayOfWeekId']
                name: str = f'R{week}_{day}'

                if not os.path.exists(newpath):
                    os.makedirs(newpath)

                file: str = os.path.join(newpath, name + ".yaml")

                if w['taskWorkout']:
                    workout_id: str = w['taskWorkout']['workoutId']
                    workout: dict = connection.get_workout(workout_id)
                    logging.info("Exporting workout '%s' into '%s'", name, file)
                    workout_export_yaml(workout, file)
                if w['taskNote']:
                    config = {}
                    config['name'] = w['taskNote']['note']
                    config['content'] = w['taskNote']['noteDescription']
                    note = Note(config)
                    logging.info("Exporting note '%s' into '%s'", name, file)
                    note_export_yaml(note, file)

            connection.delete_training_plan(tp['trainingPlanId'])


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
        username=account.USERNAME,
        password=account.PASSWORD)


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

    pzones, rpower_zones, cpower_zones, pdata = Power.power_zones(account.rFTP, account.cFTP)

    with _garmin_client(args) as connection:
        connection.save_hr_zones(data)
        connection.save_power_zones(pdata)

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
    parser_import.add_argument("trainingplan",
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

    parser_delete = subparsers.add_parser("activity-list",
                                          description="Activity list")
    parser_delete.set_defaults(func=command_activity_list)

    parser_delete = subparsers.add_parser("find-events",
                                          description="Find events")
    parser_delete.set_defaults(func=command_find_events)

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
