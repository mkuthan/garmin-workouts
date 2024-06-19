from datetime import date, timedelta


def get_date(name, race) -> tuple[date, int, int]:
    if '_' in name:
        if name.startswith('R'):
            ind = 1
            week: int = -int(name[ind:name.index('_')])
            day = int(name[name.index('_') + 1:name.index('_') + 2])
        else:
            ind = 0
            week = int(name[ind:name.index('_')])
            day = int(name[name.index('_') + 1:name.index('_') + 2])
        return race - timedelta(weeks=week + 1) + timedelta(days=day), week, day
    else:
        return date.today(), 0, 0
