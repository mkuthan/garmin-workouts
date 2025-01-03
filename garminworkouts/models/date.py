from datetime import date, timedelta


def get_date(name, race, date_ini) -> tuple[date, int, int]:
    try:
        week: int = int(name[1:name.index('_')]) if name.startswith('R') else int(name.split('_')[0])
        week: int = -week if name.startswith('R') or 'D' in name else week
        day: int = int(name.split('_')[1][0]) if '_' in name else int(name.split('D')[1].split('-')[0])
        return race - timedelta(weeks=week + 1) + timedelta(days=day), week, day
    except ValueError:
        if isinstance(date_ini, dict):
            return date(
                year=date_ini.get('year', 2024),
                month=date_ini.get('month', 1),
                day=date_ini.get('day', 1)), 0, 0
        else:
            return date.today(), 0, 0
