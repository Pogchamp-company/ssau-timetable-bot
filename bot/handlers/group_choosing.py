import aiogram.utils.markdown as md
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.app import Form, dp, bot
from bot.cached_data import get_facilities, get_groups
from bot.markups import get_institutes_markup, get_groups_markup, get_actions_markup


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await Form.institute.set()

    institutes_kb = await get_institutes_markup()

    await message.answer("Привет, выбери институт или факультет", reply_markup=institutes_kb)


@dp.message_handler(state=Form.institute)
async def process_institute(message: types.Message, state: FSMContext):
    institutes = await get_facilities()

    if message.text not in institutes:
        await message.reply("Такой институт не найден")
        return

    await Form.next()
    await state.update_data(institute=message.text)

    courses_kb = ReplyKeyboardMarkup([[KeyboardButton(str(i)) for i in range(1, 6)]])

    await message.answer("Выберите курс (от 1 до 5)", reply_markup=courses_kb)


@dp.message_handler(lambda message: message.text not in ['1', '2', '3', '4', '5'], state=Form.course)
async def failed_process_age(message: types.Message):
    return await message.answer("Курс должен быть числом от 1 до 5.\nВыберите курс (от 1 до 5)")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.course)
async def process_course(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(course=int(message.text))

    data = await state.get_data()

    groups_kb = await get_groups_markup(data['institute'], int(data['course']))

    await message.answer("Выберите код группы", reply_markup=groups_kb)


@dp.message_handler(state=Form.group_code)
async def process_group_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    groups = await get_groups(data['institute'], int(data['course']))
    if message.text not in groups:
        await message.answer("Такая группа не найдена")
        return

    await Form.next()
    await state.update_data(group_code=message.text)
    await state.update_data(group_id=groups[message.text])

    # Remove keyboard
    actions_kb = get_actions_markup()

    data = await state.get_data()

    # And send message
    await bot.send_message(message.chat.id, md.text(
        md.text('Выбран ', md.bold(data['institute'])),
        md.text('Курс:', data['course']),
        md.text('Код группы:', data['group_code']),
        sep='\n'), reply_markup=actions_kb, parse_mode=ParseMode.MARKDOWN)
