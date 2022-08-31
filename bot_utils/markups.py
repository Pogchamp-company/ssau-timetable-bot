from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot_utils.cached_data import get_facilities, get_groups


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
