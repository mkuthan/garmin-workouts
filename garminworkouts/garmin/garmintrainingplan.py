from requests import Response
from garminworkouts.garmin.garminactivity import GarminActivity
from garminworkouts.models.trainingplan import TrainingPlan
import account


class GarminTrainingplan(GarminActivity):
    _TRAINING_PLAN_SERVICE_ENDPOINT = "/trainingplan-service/trainingplan"

    def list_trainingplans(self, locale) -> dict:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/search"
        params: dict = {
            "start": '1',
            "limit": '1000',
            "locale": locale.split('-')[0],
        }
        headers: dict = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        return self.post(url, params=params, api=True, headers=headers).json().get('trainingPlanList')

    def schedule_training_plan(self, plan_id, startDate) -> dict:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/schedule/{plan_id}"
        params: dict = {
            "startDate": startDate,
        }
        return self.get(url, params=params).json()

    def get_training_plan(self, plan_id) -> dict:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/tasks/{plan_id}"
        return self.get(url).json()

    def delete_training_plan(self, plan_id) -> Response:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/trainingplan/{plan_id}"
        return self.delete(url)

    def delete_training_plan_workout(self, plan_id, workout_id) -> Response:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/workoutTask/{plan_id}/{workout_id}"
        return self.delete(url)

    def delete_training_plan_note(self, plan_id, note_id) -> Response:
        url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/noteTask/{plan_id}/{note_id}"
        return self.delete(url)

    def trainingplan_list(self) -> None:
        for tp in self.list_trainingplans(account.locale):
            TrainingPlan.print_trainingplan_summary(tp)
