import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.files import PickleStorage, JSONStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    ParseMode
import aiogram.utils.markdown as md

from dotenv import load_dotenv

from bot_utils.cached_data import get_facilities, get_groups
from bot_utils.markups import get_institutes_markup, get_groups_markup

load_dotenv()

API_TOKEN = os.environ.get("BOT_TOKEN")


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("My_app")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = JSONStorage('bot.json')
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    institute = State()
    course = State()
    group_code = State()
    timetable = State()


@dp.message_handler(commands=['start', 'help'])
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

    # Remove keyboard
    actions_kb = ReplyKeyboardMarkup(
        [
            [KeyboardButton('Расписание на эту неделю'),
             KeyboardButton('Расписание на следующую неделю'),
             KeyboardButton('Расписание на завтра'), ],
            [KeyboardButton('Выбрать другое направление')]
        ]
    )

    data = await state.get_data()

    # And send message
    await bot.send_message(message.chat.id, md.text(
        md.text('Выбран ', md.bold(data['institute'])),
        md.text('Курс:', data['course']),
        md.text('Код группы:', data['group_code']),
        sep='\n'), reply_markup=actions_kb, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(lambda message: message.text == 'Выбрать другое направление', state=Form.timetable)
async def send_another(message: types.Message, state: FSMContext):
    logger.info('fghfhgjkdhgjjhdgkjhdkjghdhgdg')
    await Form.institute.set()
    await state.reset_data()

    institutes_kb = await get_institutes_markup()

    await message.answer("Выбери институт или факультет", reply_markup=institutes_kb)


if __name__ == '__main__':
    executor.start_polling(dp)
