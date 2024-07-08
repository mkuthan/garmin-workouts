from requests import Response
from garminworkouts.garmin.garmintrainingplan import GarminTrainingplan
from garminworkouts.models.extraction import Extraction


class GarminNote(GarminTrainingplan):
    _CALENDAR_SERVICE_ENDPOINT = "/calendar-service"

    def get_note(self, trainingplan, note_id) -> Response:
        if trainingplan:
            url: str = f"{self._TRAINING_PLAN_SERVICE_ENDPOINT}/scheduled/notes/{note_id}"
        else:
            url: str = f"{self._CALENDAR_SERVICE_ENDPOINT}/note/{note_id}"
        return self.get(url)

    def save_note(self, note) -> dict:
        url: str = f"{self._CALENDAR_SERVICE_ENDPOINT}/note"
        return self.post(url, json=note).json()

    def update_note(self, note_id, note) -> Response:
        url: str = f"{self._CALENDAR_SERVICE_ENDPOINT}/note/{note_id}"
        return self.put(url, json=note)

    def delete_note(self, note_id) -> Response:
        url: str = f"{self._CALENDAR_SERVICE_ENDPOINT}/note/{note_id}"
        return self.delete(url)

    def download_note_yaml(self, trainingplan, note_id, filename) -> dict:
        note_data: dict = self.get_note(trainingplan, note_id).json()
        Extraction.note_export_yaml(note_data, filename)
        return note_data
