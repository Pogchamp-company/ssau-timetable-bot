import datetime


def get_current_week_number() -> int:
    return datetime.datetime.now().isocalendar()[1] - datetime.datetime(2022, 9, 1).isocalendar()[1] + 1


def get_weekday_from_date(date: datetime.date):
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    return weekdays[date.weekday()]
