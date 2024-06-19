import unittest
from datetime import date, timedelta
from garminworkouts.models.note import Note


class TestNote(unittest.TestCase):

    def setUp(self) -> None:
        self.config: dict = {
            'id': '123',
            'name': 'Race_2_5',
            'content': 'Sample content',
            'date': None,
            }
        self.note = Note(self.config)

    def test_get_note_name(self) -> None:
        self.assertEqual(self.note.get_note_name(), 'Race_2_5')

    def test_create_note(self) -> None:
        expected_output: dict = {'id': '123', 'noteName': 'Race_2_5', 'content': 'Sample content', 'date': None}
        self.assertEqual(self.note.create_note(self.config.get('id')), expected_output)

    def test_print_note_summary(self) -> None:
        self.assertEqual(self.note.print_note_summary(), None)

    def test_get_note_date_with_week(self) -> None:
        config: dict[str, str] = {'name': 'R1_3', 'content': 'Sample content'}
        note = Note(config)
        expected_output: tuple = (date.today() - timedelta(weeks=0) + timedelta(days=3), -1, 3)
        self.assertEqual(note.get_note_date(), expected_output)

    def test_extract_note_id(self) -> None:
        self.assertEqual(self.note.extract_note_id(), '123')

    def test_get_note_date_default(self) -> None:
        config: dict[str, str] = {'name': 'SampleNote', 'content': 'Sample content'}
        note = Note(config)
        expected_output: tuple = (date.today(), 0, 0)
        self.assertEqual(note.get_note_date(), expected_output)

    def test_get_note_content(self) -> None:
        self.assertEqual(self.note.get_note_content(), 'Sample content')

    def test_get_note_content_empty(self) -> None:
        config: dict[str, str] = {'name': 'Race_2_5'}
        note = Note(config)
        self.assertEqual(note.get_note_content(), '')

    def test_get_note_content_custom(self) -> None:
        config: dict[str, str] = {'name': 'Race_2_5', 'content': 'Custom content'}
        note = Note(config)
        self.assertEqual(note.get_note_content(), 'Custom content')


if __name__ == '__main__':
    unittest.main()
