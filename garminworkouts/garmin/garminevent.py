from datetime import datetime, timedelta
import json
import os
from typing import Any, Generator
from requests import Response
from garminworkouts.garmin.garminnote import GarminNote
from garminworkouts.models.event import Event
from garminworkouts.models.extraction import Extraction


class GarminEvent(GarminNote):

    def list_events(self, batch_size=20) -> Generator[dict, dict, None]:
        url: str = f"{self._CALENDAR_SERVICE_ENDPOINT}/events"
        start_index = 1
        all_events_fetched = False
        while not all_events_fetched:
            params: dict = {
                "startDate": datetime.today(),
                "pageIndex": start_index,
                "limit": batch_size
            }
            response: dict = self.get(url, params=params).json()
            if not response or response == []:
                all_events_fetched = True
            else:
                for response_json in response:
                    yield response_json
            start_index += batch_size

    def get_event(self, event_id) -> dict:
        url: str = f"{self._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"
        return self.get(url).json()

    def save_event(self, event) -> dict:
        url: str = f"{self._CALENDAR_SERVICE_ENDPOINT}/event"
        return self.post(url, json=event).json()

    def update_event(self, event_id, event) -> Response:
        url: str = f"{self._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"
        return self.put(url, json=event)

    def delete_event(self, event_id) -> Response:
        url: str = f"{self._CALENDAR_SERVICE_ENDPOINT}/event/{event_id}"
        return self.delete(url)

    def event_list(self) -> None:
        for event in self.list_events():
            Event.print_event_summary(event)

    def find_events(self) -> Generator[dict, Any, None]:
        url = "race-search/events"

        d1 = datetime.today()
        d2 = d1 + timedelta(days=7)

        params: dict = {
            "eventType": "running",
            "fromDate": d1.strftime('%Y-%m-%d'),
            "toDate": d2.strftime('%Y-%m-%d'),
            "includeInPerson": True,
            "includeVirtual": False,
            "verifiedStatuses": "OFFICIAL,VERIFIED",  # ,NONE
            "includeNst": True,
            "limit": 200,
            "eventsProviders": "garmin-events,gc-discoverable-events,garmin-official-events,ahotu",
            "completionTargetMinValue": 41000,
            "completionTargetMaxValue": 43000,
            "completionTargetDurationType": "distance"
        }

        while True:
            params['fromDate'] = d1.strftime('%Y-%m-%d')
            params['toDate'] = d2.strftime('%Y-%m-%d')
            ev: dict = self.get(url, params=params).json()
            if ev:
                yield ev
                d1: datetime = d2
                d2: datetime = d1 + timedelta(days=7)
            else:
                break

    def _find_events(self) -> None:
        events: Generator[dict, Any, None] = self.find_events()
        for subev in events:
            for ev in subev:
                if isinstance(ev, bytes):
                    ev: dict = json.loads(ev.decode('utf-8'))
                if ('administrativeArea' in ev) and\
                    (ev.get('administrativeArea', {}) is not None) and\
                        (ev.get('administrativeArea', {}).get('countryCode') is not None):
                    newpath: str = os.path.join('.', 'exported', 'events',
                                                ev.get('eventType', ''),
                                                ev.get('administrativeArea', {}).get('countryCode', ''))
                else:
                    newpath: str = os.path.join('.', 'exported', 'events', ev.get('eventType', ''))
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                file: str = os.path.join(newpath, ev.get('eventRef', '') + '.yaml')
                Extraction.event_export_yaml(event=self.get(ev.get('detailsEndpoints', '')[0].get('url', '')
                                                            ).json(), filename=file)
