import datetime


def get_current_week_number() -> int:
    return datetime.datetime.now().isocalendar()[1] - datetime.datetime(2022, 9, 1).isocalendar()[1] + 1
