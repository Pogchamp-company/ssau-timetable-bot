import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

API_TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
storage = JSONStorage('data/bot.json')
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    institute = State()
    course = State()
    group_code = State()
    timetable = State()
