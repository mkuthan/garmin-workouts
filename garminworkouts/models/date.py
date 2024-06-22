from datetime import date, timedelta


def get_date(name, race, date_ini) -> tuple[date, int, int]:
    try:
        if name.startswith('R'):
            week: int = -int(name[1:name.index('_')])
        else:
            week = int(name[0:name.index('_')])
        day = int(name[name.index('_') + 1:name.index('_') + 2])
        return race - timedelta(weeks=week + 1) + timedelta(days=day), week, day
    except ValueError:
        if isinstance(date_ini, dict):
            return date(
                year=date_ini.get('year', 2024),
                month=date_ini.get('month', 1),
                day=date_ini.get('day', 1)), 0, 0
        else:
            return date.today(), 0, 0
