from datetime import date, timedelta


class Note(object):
    def __init__(
            self,
            config,
            race=date.today()
            ) -> None:

        self.config: dict = config
        self.name = config.get('name', '')
        self.content = config.get('content', '')
        self.race: date = race

    def get_note_name(self) -> str:
        return str(self.config.get('name'))

    @staticmethod
    def extract_note_id(note) -> str:
        return note.get('id')

    @staticmethod
    def extract_note_date(note) -> str:
        return note.get('date', '')

    @staticmethod
    def extract_note_name(note) -> str:
        return note.get('noteName')

    @staticmethod
    def extract_note_content(note) -> str:
        return note.get('content')

    def create_note(self, id=None, date=None) -> dict:
        return {
            'id': id,
            'noteName': self.name,
            'content': self.content,
            'date': date
        }

    @staticmethod
    def print_note_summary(note) -> None:
        note_id: str = Note.extract_note_id(note)
        note_name: str = Note.extract_note_name(note)
        note_content: str = Note.extract_note_content(note)
        print('{0} {1:20} {2}'.format(note_id, note_name, note_content))

    def get_note_date(self) -> tuple[date, int, int]:
        note_name: str = self.config.get('name', '')
        if '_' in note_name:
            if note_name.startswith('R'):
                ind = 1
                week: int = -int(note_name[ind:note_name.index('_')])
                day = int(note_name[note_name.index('_') + 1:note_name.index('_') + 2])
            else:
                ind = 0
                week = int(note_name[ind:note_name.index('_')])
                day = int(note_name[note_name.index('_') + 1:note_name.index('_') + 2])

            return self.race - timedelta(weeks=week + 1) + timedelta(days=day), week, day
        else:
            return date.today(), int(0), int(0)
