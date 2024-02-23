from datetime import date
from garminworkouts.models.fields import _WORKOUT_ID, _EVENT_NAME, _DATE, _NAME, _COURSE
from garminworkouts.models.fields import _LOCATION, _EVENT_TIME, _ID, _COURSE_ID, _SPORT, _GOAL
from garminworkouts.models.duration import Duration
from garminworkouts.utils import functional
import json


class Event(object):
    def __init__(
            self,
            config
    ) -> None:

        self.name: str = config.get(_NAME)
        self.date = date(config.get(_DATE).get('year'), config.get(_DATE).get('month'), config.get(_DATE).get('day'))
        self.url: str | None = config.get('url')
        self.location: str | None = config.get(_LOCATION)
        self.time: str | None = config.get('time')
        self.distance: str | None = config.get('distance')
        self.goal: int | None = Duration(config.get(_GOAL)).to_seconds() if _GOAL in config else None
        self.course: str | None = config.get(_COURSE)
        self.sport: str = config.get(_SPORT)

    @staticmethod
    def extract_event_id(event) -> str:
        return event.get(_ID)

    @staticmethod
    def extract_event_name(event) -> str:
        return event.get(_EVENT_NAME)

    @staticmethod
    def extract_event_date(event) -> str:
        return event.get(_DATE)

    @staticmethod
    def extract_event_location(event) -> str:
        return event.get(_LOCATION)

    @staticmethod
    def extract_event_time(event) -> str:
        return event.get(_EVENT_TIME)

    @staticmethod
    def extract_course(event) -> str:
        return event.get(_COURSE_ID)

    @staticmethod
    def print_event_summary(event) -> None:
        event_id: str = Event.extract_event_id(event)
        event_name: str = Event.extract_event_name(event)
        event_date: str = Event.extract_event_date(event)
        event_location: str = Event.extract_event_location(event)
        print("{0} {1:20} {2:10} {3}".format(event_id, event_name, event_location, event_date))

    @staticmethod
    def print_event_json(event) -> None:
        print(json.dumps(functional.filter_empty(event)))

    def create_event(self, event_id=None, workout_id=None) -> dict:
        return {
            _ID: event_id,
            _EVENT_NAME: self.name,
            _DATE: str(self.date),
            'url': self.url,
            'registrationUrl': None,
            _COURSE_ID: self.course,
            'completionTarget': {
                'value': self.distance,
                'unit': 'kilometer',
                'unitType': 'distance'
            },
            _EVENT_TIME: {
                'startTimeHhMm': self.time,
                'timeZoneId': 'Europe/Paris'
            },
            'note': None,
            _WORKOUT_ID: workout_id,
            _LOCATION: self.location,
            'eventType': self.sport,
            'eventPrivacy': {
                'label': 'PRIVATE',
                'isShareable': False,
                'isDiscoverable': False
            },
            'shareableEventUuid': None,
            'eventCustomization': {
                'customGoal': {
                    'value': self.goal,
                    'unit': 'second',
                    'unitType': 'time'},
                'isPrimaryEvent': None,
                'isTrainingEvent': True},
            'race': True,
            'eventOrganizer': True,
            'subscribed': True
        }
