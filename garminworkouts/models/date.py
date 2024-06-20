from datetime import date, timedelta


def get_date(name, race) -> tuple[date, int, int]:
    try:
        if name.startswith('R'):
            week: int = -int(name[1:name.index('_')])
        else:
            week = int(name[0:name.index('_')])
        day = int(name[name.index('_') + 1:name.index('_') + 2])
        return race - timedelta(weeks=week + 1) + timedelta(days=day), week, day
    except ValueError:
        return date.today(), 0, 0
