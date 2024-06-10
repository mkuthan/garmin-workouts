import pytest
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.workout import Workout
from garminworkouts.models.event import Event
from datetime import date, timedelta
from typing import Any
from requests import Response
import os
from garminworkouts.models.settings import settings
from garminworkouts.models.yoga import YOGA_POSES
from garminworkouts.models.strength import STRENGTH_EXERCISES
from garminworkouts.models.fields import get_step_type, get_sport_type, get_end_condition, get_intensity_type
from garminworkouts.models.fields import get_target_type, get_equipment_type, get_stroke_type, get_swim_instruction_type
from garminworkouts.models.fields import get_drill_type, get_activity_type, get_event_type


class Arg(object):
    def __init__(
        self,
        trainingplan
    ) -> None:
        self.trainingplan = trainingplan


@pytest.mark.vcr
def test_external_workouts(authed_gclient: GarminClient) -> None:
    locale = 'en-US'
    authed_gclient.external_workouts(locale)


@pytest.mark.vcr
def test_get_external_workout(authed_gclient: GarminClient) -> None:
    locale = 'en-US'
    workouts: dict = authed_gclient.external_workouts(locale)

    for workout in workouts:
        assert authed_gclient.get_external_workout(workout['workoutSourceId'], locale)


@pytest.mark.vcr
def test_list_workouts(authed_gclient: GarminClient) -> None:
    assert authed_gclient.list_workouts()


@pytest.mark.vcr
def test_get_calendar(authed_gclient: GarminClient) -> None:
    year = str(date.today().year)
    month = str(date.today().month - 1)
    url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}"

    assert authed_gclient.get(url)

    updateable_elements, checkable_elements, note_elements = authed_gclient.get_calendar(date.today())
    assert len(updateable_elements) >= 0
    assert len(checkable_elements) >= 0
    assert len(note_elements) >= 0


@pytest.mark.vcr
def test_list_events(authed_gclient: GarminClient) -> None:
    assert authed_gclient.list_events()


@pytest.mark.vcr
def test_events_methods(authed_gclient: GarminClient) -> None:
    event_config: dict = {
        'name': 'Name',
        'date': {
            'day': int(1),
            'month': int(date.today().month),
            'year': int(date.today().year + 1),
        },
        'url': 'https://www.123.com/',
        'location': 'London, UK',
        'time': '19:00',
        'distance': 5,
        'goal': '20:00',
        'sport': 'running'}

    event = Event(event_config)
    e: dict = event.create_event()
    assert e
    e = authed_gclient.save_event(e)
    assert e
    event_id = Event.extract_event_id(e)
    assert authed_gclient.get_event(event_id)
    assert authed_gclient.update_event(event_id, e)
    assert authed_gclient.delete_event(event_id)


@pytest.mark.vcr
def test_get_activities_by_date(authed_gclient: GarminClient) -> None:
    startdate: date = date.today() + timedelta(weeks=-4)
    enddate: str = date.today().isoformat()
    activitytype = None

    activities: list = []
    start = 0
    limit = 20

    url: str = f"{GarminClient._ACTIVITY_LIST_SERVICE_ENDPOINT}/activities/search/activities"
    params: dict[str, str] = {
        "startDate": str(startdate),
        "endDate": str(enddate),
        "start": str(start),
        "limit": str(limit),
    }
    if activitytype:
        params["activityType"] = str(activitytype)

    print(f"Requesting activities by date from {startdate} to {enddate}")
    while True:
        params["start"] = str(start)
        print(f"Requesting activities {start} to {start+limit}")
        act: Response = authed_gclient.get(url, params=params)
        assert act
        if act.json() != []:
            activities.extend(act)
            start = start + limit
        else:
            break


@pytest.mark.vcr
def test_list_workout_types(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/types"
    types: dict = authed_gclient.get(url).json()
    assert types

    for i in range(len(types['workoutStepTypes'])):
        types['workoutStepTypes'][i].pop('displayOrder')
        assert types['workoutStepTypes'][i] == get_step_type(types['workoutStepTypes'][i]['stepTypeKey'])

    for i in range(len(types['workoutSportTypes'])):
        types['workoutSportTypes'][i].pop('displayOrder')
        assert types['workoutSportTypes'][i] == get_sport_type(types['workoutSportTypes'][i]['sportTypeKey'])

    for i in range(len(types['workoutConditionTypes'])):
        types['workoutConditionTypes'][i].pop('displayOrder')
        types['workoutConditionTypes'][i].pop('displayable')
        assert types['workoutConditionTypes'][i] == get_end_condition(
            types['workoutConditionTypes'][i]['conditionTypeKey'])

    for i in range(len(types['workoutIntensityTypes'])):
        types['workoutIntensityTypes'][i].pop('displayOrder')
        assert types['workoutIntensityTypes'][i] == get_intensity_type(
            types['workoutIntensityTypes'][i]['intensityTypeKey'])

    for i in range(len(types['workoutTargetTypes'])):
        types['workoutTargetTypes'][i].pop('displayOrder')
        assert types['workoutTargetTypes'][i] == get_target_type(
            types['workoutTargetTypes'][i]['workoutTargetTypeKey'])

    for i in range(len(types['workoutEquipmentTypes'])):
        types['workoutEquipmentTypes'][i].pop('displayOrder')
        assert types['workoutEquipmentTypes'][i] == get_equipment_type(
            types['workoutEquipmentTypes'][i]['equipmentTypeKey'])

    for i in range(len(types['workoutStrokeTypes'])):
        types['workoutStrokeTypes'][i].pop('displayOrder')
        assert types['workoutStrokeTypes'][i] == get_stroke_type(
            types['workoutStrokeTypes'][i]['strokeTypeKey'])

    for i in range(len(types['workoutSwimInstructionTypes'])):
        types['workoutSwimInstructionTypes'][i].pop('displayOrder')
        assert types['workoutSwimInstructionTypes'][i] == get_swim_instruction_type(
            types['workoutSwimInstructionTypes'][i]['swimInstructionTypeKey'])

    for i in range(len(types['workoutDrillTypes'])):
        types['workoutDrillTypes'][i].pop('displayOrder')
        assert types['workoutDrillTypes'][i] == get_drill_type(
            types['workoutDrillTypes'][i]['drillTypeKey'])


@pytest.mark.vcr
def test_get_activity_types(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/activityTypes"
    activities: dict = authed_gclient.get(url).json()
    assert activities

    for i in range(len(activities)):
        activities[i].pop('parentTypeId')
        activities[i].pop('isHidden')
        activities[i].pop('restricted')
        activities[i].pop('trimmable')
        assert activities[i] == get_activity_type(
            activities[i]['typeKey'])


@pytest.mark.vcr
def test_get_event_types(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/eventTypes"
    events: dict = authed_gclient.get(url).json()
    assert events

    for i in range(len(events)):
        events[i].pop('sortOrder')
        assert events[i] == get_event_type(
            events[i]['typeKey'])


@pytest.mark.vcr
def test_get_golf_types(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._GOLF_COMMUNITY_ENDPOINT}/types"
    golf: dict = authed_gclient.get(url).json()
    assert golf


@pytest.mark.vcr
def test_get_strength_types(authed_gclient: GarminClient) -> None:
    url: str = "/web-data/exercises/Exercises.json"
    strength: dict = authed_gclient.garth.get("connect", url).json()['categories']
    assert strength

    assert STRENGTH_EXERCISES == strength


@pytest.mark.vcr
def test_get_yoga_types(authed_gclient: GarminClient) -> None:
    url: str = "/web-data/exercises/Yoga.json"
    yoga: dict = authed_gclient.garth.get("connect", url).json()['categories']
    assert yoga

    keysList = list(yoga.keys())
    for key in keysList:
        assert YOGA_POSES[key] == yoga[key]['exercises']


@pytest.mark.vcr
def test_get_RHR(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._WELLNESS_SERVICE_ENDPOINT}/wellness/dailyHeartRate"
    params: dict = {
       "date": date.today(),
    }
    assert authed_gclient.get(url, params=params)


@pytest.mark.vcr
def test_get_hr_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
    assert authed_gclient.get(url)


@pytest.mark.vcr
def test_save_hr_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
    zones: dict = authed_gclient.get(url).json()
    assert authed_gclient.put(url, json=zones)


@pytest.mark.vcr
def test_get_power_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/sports/all"
    assert authed_gclient.get(url)


@pytest.mark.vcr
def test_save_power_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/all"
    zones: list[dict[str, Any]] = [
        {
            "sport": "CYCLING",
            "functionalThresholdPower": str(275),
            "zone1Floor": str(179),
            "zone2Floor": str(220),
            "zone3Floor": str(248),
            "zone4Floor": str(275),
            "zone5Floor": str(316),
            "zone6Floor": str(358),
            "zone7Floor": str(412),
            "userLocalTime": None
        },
        {
            "sport": "RUNNING",
            "functionalThresholdPower": str(380),
            "zone1Floor": str(247),
            "zone2Floor": str(304),
            "zone3Floor": str(342),
            "zone4Floor": str(380),
            "zone5Floor": str(437),
            "zone6Floor": str(0.0),
            "zone7Floor": str(0.0),
            "userLocalTime": None
        }
    ]
    assert authed_gclient.put(url, json=zones)


@pytest.mark.vcr
def test_workout_list(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workouts"
    params: dict[str, Any] = {
        "start": 0,
        "limit": 20,
        "myWorkoutsOnly": False,
        "sharedWorkoutsOnly": False,
        "orderBy": "WORKOUT_NAME",
        "orderSeq": "ASC",
        "includeAtp": True
        }
    assert authed_gclient.get(url, params=params)


@pytest.mark.vcr
def test_trainingplan_garmin_workouts(authed_gclient: GarminClient) -> None:
    tp_list: list[str] = [
        os.path.join('workouts', 'strength_training', 'ADVANCED', '*.yaml'),
        os.path.join('workouts', 'strength_training', 'INTERMEDIATE', '*.yaml'),
        os.path.join('workouts', 'strength_training', 'BEGINNER', '*.yaml'),
        os.path.join('workouts', 'cardio_training', 'ADVANCED', '*.yaml'),
        os.path.join('workouts', 'cardio_training', 'INTERMEDIATE', '*.yaml'),
        os.path.join('workouts', 'cardio_training', 'BEGINNER', '*.yaml'),
        os.path.join('workouts', 'hiit', 'ADVANCED', '*.yaml'),
        os.path.join('workouts', 'hiit', 'INTERMEDIATE', '*.yaml'),
        os.path.join('workouts', 'hiit', 'BEGINNER', '*.yaml'),
        os.path.join('workouts', 'pilates', 'ADVANCED', '*.yaml'),
        os.path.join('workouts', 'pilates', 'INTERMEDIATE', '*.yaml'),
        os.path.join('workouts', 'pilates', 'BEGINNER', '*.yaml'),
        os.path.join('workouts', 'yoga', 'INTERMEDIATE', '*.yaml'),
        os.path.join('workouts', 'yoga', 'BEGINNER', '*.yaml'),
        ]

    for tp in tp_list:
        args = Arg(trainingplan=tp)
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
