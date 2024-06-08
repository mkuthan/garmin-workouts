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
            'eventTimeLocal': '10:00',
            'distance': '10 km',
            'goal': '1:00:00',
            'course': 'Test Course',
            'sport': 'Running'
        }
        self.event = Event(self.event_config)

    def test_extract_event_id(self) -> None:
        self.assertEqual(Event.extract_event_id({'id': '123'}), '123')

    def test_extract_event_name(self) -> None:
        self.assertEqual(Event.extract_event_name({'eventName': 'Test Event'}), 'Test Event')

    def test_extract_event_date(self) -> None:
        self.assertEqual(Event.extract_event_date({'date': {'year': 2022, 'month': 1, 'day': 1}}), date(2022, 1, 1))

    def test_extract_event_location(self) -> None:
        self.assertEqual(Event.extract_event_location({'location': 'Test Location'}), 'Test Location')

    def test_extract_event_time(self) -> None:
        self.assertEqual(Event.extract_event_time({'eventTimeLocal': '10:00'}), '10:00')

    def test_extract_course(self) -> None:
        self.assertEqual(Event.extract_course({'courseId': '456'}), '456')

    def test_print_event_summary(self) -> None:
        self.assertEqual(Event.print_event_summary(self.event_config), None)

    def test_print_event_json(self) -> None:
        self.assertEqual(Event.print_event_json(self.event_config), None)

    def test_create_event(self) -> None:
        self.setUp()
        event_data: dict = self.event.create_event(event_id='123', workout_id='456')
        self.assertEqual(event_data['id'], '123')
        self.assertEqual(event_data['eventName'], 'Test Event')
        self.assertEqual(event_data['date'], '2022-01-01')
        self.assertEqual(event_data['courseId'], 'Test Course')
        self.assertEqual(event_data['eventPrivacy']['isShareable'], False)
        self.assertEqual(event_data['eventCustomization']['customGoal']['value'], 3600)


if __name__ == '__main__':
    unittest.main()
