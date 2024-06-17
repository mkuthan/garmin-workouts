import os
from datetime import date
import argparse
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.workout import Workout
from garminworkouts.models.settings import settings
from trainingplans.lists import WorkoutsList


def test_external_workouts(authed_gclient: GarminClient) -> None:
    locale = 'en-US'
    authed_gclient.external_workouts(locale)


def test_get_external_workout(authed_gclient: GarminClient) -> None:
    locale = 'en-US'
    workouts: dict = authed_gclient.external_workouts(locale)

    for workout in workouts:
        assert authed_gclient.get_external_workout(workout['workoutSourceId'], locale)


def test_list_workouts(authed_gclient: GarminClient) -> None:
    assert authed_gclient.list_workouts()


def test_trainingplan_garmin_workouts(authed_gclient: GarminClient) -> None:
    for tp in WorkoutsList:
        args = argparse.Namespace(trainingplan=tp)
        workouts, *_ = settings(args)

        for workout in workouts:
            payload: dict = workout.create_workout()
            assert payload
            w: dict = authed_gclient.save_workout(payload)
            assert w
            workout_id: str = Workout.extract_workout_id(w)
            assert workout_id
            payload = workout.create_workout(workout_id=workout_id)
            assert payload
            assert authed_gclient.update_workout(workout_id, payload)
            assert authed_gclient.get_workout(workout_id)
            assert authed_gclient.download_workout(workout_id, f"{workout_id}.fit")
            os.remove(f"{workout_id}.fit")
            assert authed_gclient.download_workout_yaml(workout_id, f"{workout_id}.yaml")
            os.remove(f"{workout_id}.yaml")
            p: dict = authed_gclient.schedule_workout(workout_id, date.today().isoformat())
            assert p['workoutScheduleId']
            assert authed_gclient.remove_workout(p['workoutScheduleId'], date.today().isoformat())
            assert authed_gclient.delete_workout(workout_id)
