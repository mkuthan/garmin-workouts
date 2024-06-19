from garminworkouts.garmin.garminclient import GarminClient


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
