class Note(object):
    def __init__(
            self,
            config
            ) -> None:

        self.name = config.get('name')
        self.content = config.get('content')

    @staticmethod
    def extract_note_name(note) -> str:
        return note.get('noteName')

    @staticmethod
    def extract_note_date(note) -> str:
        return note.get('date')

    def create_note(self, id=None, date=None) -> dict:
        return {
            'id': id,
            'noteName': self.name,
            'content': self.content,
            'date': date
        }
