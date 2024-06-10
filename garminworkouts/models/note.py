from datetime import date, timedelta


class Note:
    def __init__(self, config, race=date.today()) -> None:
        self.config = config
        self.name = config.get('name', '')
        self.content = config.get('content', '')
        self.race: date = race

    def get_note_name(self) -> str:
        return str(self.config.get('name'))

    def create_note(self, id=None, date=None) -> dict:
        return {
            'id': id,
            'noteName': self.name,
            'content': self.content,
            'date': date
        }

    def extract_note_id(self) -> str:
        return self.config.get('id', '')

    def print_note_summary(self) -> None:
        note_id: str = self.config.get('id')
        note_name: str = self.config.get('name')
        note_content: str = self.config.get('content')
        print(f'{note_id} {note_name:20} {note_content}')

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
            return date.today(), 0, 0
