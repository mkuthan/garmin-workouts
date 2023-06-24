from datetime import date
from garminworkouts.models.fields import _WORKOUT_ID_FIELD, _EVENT_ID_FIELD, _EVENT_NAME_FIELD, _EVENT_DATE_FIELD
from garminworkouts.models.fields import _EVENT_LOCATION_FIELD, _EVENT_TIME_FIELD, _COURSE_FIELD
from garminworkouts.models.duration import Duration
from garminworkouts.utils import functional
import json


class Event(object):
    def __init__(
            self,
            config
            ):

        self.name = config['name']
        self.date = date(config['date']['year'], config['date']['month'], config['date']['day'])
        self.url = config['url'] if 'url' in config else None
        self.location = config['location'] if 'location' in config else None
        self.time = config['time'] if 'time' in config else None
        self.distance = config['distance'] if 'distance' in config else None
        self.goal = Duration(config['goal']).to_seconds() if 'goal' in config else None
        self.course = config['course'] if 'course' in config else None
        self.sport = config['sport']

    @staticmethod
    def extract_event_id(event):
        return event[_EVENT_ID_FIELD]

    @staticmethod
    def extract_event_name(event):
        return event[_EVENT_NAME_FIELD]

    @staticmethod
    def extract_event_date(event):
        return event[_EVENT_DATE_FIELD]

    @staticmethod
    def extract_event_location(event):
        return event[_EVENT_LOCATION_FIELD]

    @staticmethod
    def extract_event_time(event):
        return event[_EVENT_TIME_FIELD]

    @staticmethod
    def extract_course(event):
        return event[_COURSE_FIELD]

    @staticmethod
    def print_event_summary(event):
        event_id = Event.extract_event_id(event)
        event_name = Event.extract_event_name(event)
        event_date = Event.extract_event_date(event)
        event_location = Event.extract_event_location(event)
        print("{0} {1:20} {2:10} {3}".format(event_id, event_name, event_location, event_date))

    @staticmethod
    def print_event_json(event):
        print(json.dumps(functional.filter_empty(event)))

    def create_event(self, event_id=None, workout_id=None):
        return {
            'id': event_id,
            _EVENT_NAME_FIELD: self.name,
            'date': str(self.date),
            'url': self.url,
            'registrationUrl': None,
            _COURSE_FIELD: self.course,
            'completionTarget': {
                'value': self.distance,
                'unit': 'kilometer',
                'unitType': 'distance'
                },
            _EVENT_TIME_FIELD: {
                'startTimeHhMm': self.time,
                'timeZoneId': 'Europe/Paris'
                },
            'note': None,
            _WORKOUT_ID_FIELD: workout_id,
            'location': self.location,
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
