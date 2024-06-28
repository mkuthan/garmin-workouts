from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.models.yoga import YOGA_POSES
from garminworkouts.models.fields import get_step_type, get_sport_type, get_end_condition, get_intensity_type
from garminworkouts.models.fields import get_target_type, get_equipment_type, get_stroke_type, get_swim_instruction_type
from garminworkouts.models.fields import get_drill_type, get_activity_type, get_event_type


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


def test_get_event_types(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/eventTypes"
    events: dict = authed_gclient.get(url).json()
    assert events

    for i in range(len(events)):
        events[i].pop('sortOrder')
        assert events[i] == get_event_type(
            events[i]['typeKey'])


def test_get_golf_types(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._GOLF_COMMUNITY_ENDPOINT}/types"
    golf: dict = authed_gclient.get(url).json()
    assert golf


def test_get_strength_types(authed_gclient: GarminClient) -> None:
    url: str = "/web-data/exercises/Exercises.json"
    strength: dict = authed_gclient.garth.get("connect", url).json()['categories']
    assert strength


def test_get_yoga_types(authed_gclient: GarminClient) -> None:
    url: str = "/web-data/exercises/Yoga.json"
    yoga: dict = authed_gclient.garth.get("connect", url).json()['categories']
    assert yoga

    keysList = list(yoga.keys())
    for key in keysList:
        assert YOGA_POSES[key] == yoga[key]['exercises']


def test_get_types(authed_gclient: GarminClient) -> None:
    assert not authed_gclient.get_types()
