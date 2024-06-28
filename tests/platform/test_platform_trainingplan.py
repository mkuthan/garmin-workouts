from datetime import date
from requests import Response
from garminworkouts.garmin.garminclient import GarminClient


def test_trainingplan_methods(authed_gclient: GarminClient) -> None:
    tp_list: dict = authed_gclient.list_trainingplans(locale='en-US')
    assert tp_list
    tp: dict = tp_list[0]
    tp_s: dict = authed_gclient.schedule_training_plan(plan_id=tp['trainingPlanId'], startDate=date.today().isoformat())
    assert tp_s
    tp = authed_gclient.get_training_plan(plan_id=tp['trainingPlanId'], locale='en-US')
    assert tp
    r: Response = authed_gclient.delete_training_plan(plan_id=tp_s['trainingPlanId'])
    assert r
