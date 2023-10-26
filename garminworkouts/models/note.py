class Note(object):
    def __init__(
            self,
            config
            ) -> None:

        self.name = config['name'] if 'content' in config else None
        self.content = config['content'] if 'content' in config else None

    @staticmethod
    def extract_note_name(note) -> str:
        return note["noteName"]

    @staticmethod
    def extract_note_date(note) -> str:
        return note["date"]

    def create_note(self, id=None, date=None) -> dict:
        return {
            "id": id,
            "noteName": self.name,
            "content": self.content,
            "date": date
        }
