from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.actions import TIMETABLE_FOR_CURRENT_WEEK, TIMETABLE_FOR_NEXT_WEEK, TIMETABLE_FOR_TOMORROW, \
    SELECT_ANOTHER_GROUP
from bot.cached_data import get_facilities, get_groups


async def get_institutes_markup():
    institutes = await get_facilities()
    institutes_kb = ReplyKeyboardMarkup()
    for i, k in institutes.items():
        button = KeyboardButton(i)
        institutes_kb.add(button)
    return institutes_kb


async def get_groups_markup(institute: str, course: int):
    institutes = await get_groups(institute, course)
    institutes_kb = ReplyKeyboardMarkup()
    for i, k in institutes.items():
        button = KeyboardButton(i)
        institutes_kb.add(button)
    return institutes_kb


def get_actions_markup():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(TIMETABLE_FOR_CURRENT_WEEK),
             KeyboardButton(TIMETABLE_FOR_NEXT_WEEK),
             KeyboardButton(TIMETABLE_FOR_TOMORROW)],
            [KeyboardButton(SELECT_ANOTHER_GROUP)]
        ]
    )
