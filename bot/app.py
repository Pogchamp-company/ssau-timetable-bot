import os

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.storages.SqlLiteStorage import SqlLiteStorage

API_TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
storage = SqlLiteStorage("data/bot_state.sqlite")
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    institute = State()
    course = State()
    group_code = State()
    timetable = State()
