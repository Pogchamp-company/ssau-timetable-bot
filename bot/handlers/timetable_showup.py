import datetime
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from bot.actions import SELECT_ANOTHER_GROUP, TIMETABLE_FOR_CURRENT_WEEK, TIMETABLE_FOR_NEXT_WEEK, \
    TIMETABLE_FOR_TOMORROW
from bot.app import dp, Form, bot
from bot.cached_data import get_timetable
from bot.format_timetable import format_timetable, format_day
from bot.markups import get_institutes_markup
from bot.utils import get_current_week_number


@dp.message_handler(lambda message: message.text == SELECT_ANOTHER_GROUP, state=Form.timetable)
async def send_another(message: types.Message, state: FSMContext):
    await Form.institute.set()
    await state.reset_data()

    institutes_kb = await get_institutes_markup()

    await message.answer("Выбери институт или факультет", reply_markup=institutes_kb)


@dp.message_handler(lambda message: message.text == TIMETABLE_FOR_CURRENT_WEEK, state=Form.timetable)
async def send_current_week(message: types.Message, state: FSMContext):
    week = get_current_week_number()

    data = await state.get_data()
    timetable = await get_timetable(data['group_id'], week)
    logging.info(timetable)

    await bot.send_message(message.chat.id, format_timetable(timetable), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(lambda message: message.text == TIMETABLE_FOR_NEXT_WEEK, state=Form.timetable)
async def send_next_week(message: types.Message, state: FSMContext):
    week = get_current_week_number()

    data = await state.get_data()
    timetable = await get_timetable(data['group_id'], week + 1)
    logging.info(timetable)

    await bot.send_message(message.chat.id, format_timetable(timetable), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(lambda message: message.text == TIMETABLE_FOR_TOMORROW, state=Form.timetable)
async def send_today(message: types.Message, state: FSMContext):
    week = get_current_week_number()

    data = await state.get_data()
    tomorrow = datetime.datetime.now().weekday() + 1
    if tomorrow < 6:
        timetable_for_tomorrow = (await get_timetable(data['group_id'], week))[tomorrow]
    else:
        timetable_for_tomorrow = (await get_timetable(data['group_id'], week + 1))[0]

    await bot.send_message(message.chat.id, format_day(timetable_for_tomorrow), parse_mode=ParseMode.HTML)
