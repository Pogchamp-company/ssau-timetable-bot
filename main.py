import os
import logging

from aiogram import executor
from dotenv import load_dotenv

load_dotenv()
try:
    os.mkdir('data')
except:
    pass


logging.basicConfig(level=logging.INFO)

from bot import dp

if __name__ == '__main__':
    executor.start_polling(dp)
