import unittest
from datetime import date
from garminworkouts.models.event import Event


class TestEvent(unittest.TestCase):

    def setUp(self) -> None:
        self.event_config: dict = {
            'id': '123',
            'name': 'Test Event',
            'date': {'year': 2022, 'month': 1, 'day': 1},
            'url': 'http://test.com',
            'location': 'Test Location',
            'time': '10:00',
            'distance': '10 km',
            'goal': '1:00:00',
            'course': 'Test Course',
            'sport': 'Running'
        }
        self.event = Event(self.event_config)
        self.event_data: dict = self.event.create_event(event_id='123', workout_id='456')

    def test_extract_event_id(self) -> None:
        self.setUp()
        self.assertEqual(Event.extract_event_id(self.event_data), '123')

    def test_extract_event_name(self) -> None:
        self.setUp()
        self.assertEqual(Event.extract_event_name(self.event_data), 'Test Event')

    def test_extract_event_date(self) -> None:
        self.setUp()
        self.assertEqual(Event.extract_event_date(self.event_config), date(2022, 1, 1))

    def test_extract_event_location(self) -> None:
        self.assertEqual(Event.extract_event_location(self.event_data), 'Test Location')

    def test_extract_event_time(self) -> None:
        self.setUp()
        self.assertEqual(Event.extract_event_time(self.event_data), '10:00')

    def test_extract_course(self) -> None:
        self.setUp()
        self.assertEqual(Event.extract_course(self.event_data), 'Test Course')

    def test_print_event_summary(self) -> None:
        self.setUp()
        self.assertEqual(Event.print_event_summary(self.event_data), None)

    def test_print_event_json(self) -> None:
        self.setUp()
        self.assertEqual(Event.print_event_json(self.event_data), None)

    def test_create_event(self) -> None:
        self.setUp()
        self.assertEqual(self.event_data['id'], '123')
        self.assertEqual(self.event_data['eventName'], 'Test Event')
        self.assertEqual(self.event_data['date'], '2022-01-01')
        self.assertEqual(self.event_data['courseId'], 'Test Course')
        self.assertEqual(self.event_data['eventPrivacy']['isShareable'], False)
        self.assertEqual(self.event_data['eventCustomization']['customGoal']['value'], 3600)
