from typing import List

from bot.utils import get_weekday_from_date
from structs import ScheduleForTheDay
import aiogram.utils.markdown as md


def format_timetable(timetable: List[ScheduleForTheDay]):
    return md.text(*[format_day(schedule) for schedule in timetable], sep=f'\n\n- - - - - - - - - -\n\n')


def format_day(schedule: ScheduleForTheDay):
    days_of_week = get_weekday_from_date(schedule.date)

    if not schedule.lessons:
        day_icon = '💤'
    elif all(map(lambda x: x.is_online, schedule.lessons)):
        day_icon = '🥱'
    else:
        day_icon = '⚰'

    result_text = [
        f'<b>{days_of_week} {day_icon}</b>'
    ]
    if schedule.lessons:
        formatted_lessons = []
        for lesson in schedule.lessons:
            formatted_lessons.append(
                f'{"🟢" if lesson.is_online else "🔴"} <i>{lesson.start} - {lesson.end}</i>'
                f' <i style=\"color:#fc5252;\">{lesson.title}</i>'
                f'\n{lesson.place} {lesson.teacher}'
            )
        result_text.append(md.text(*formatted_lessons, sep='\n\n'))
    else:
        result_text.append(md.text('День свободен'))
    return md.text(*result_text, sep='\n')
