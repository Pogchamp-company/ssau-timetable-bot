import logging

from aiogram import executor
from dotenv import load_dotenv

load_dotenv()

from bot.app import dp
from bot.handlers.group_choosing import *
from bot.handlers.timetable_showup import *

class CustomFormatter(logging.Formatter):
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    FORMATS = {
        logging.DEBUG: OKBLUE + format + ENDC,
        logging.INFO: OKCYAN + format + ENDC,
        logging.WARNING: WARNING + format + ENDC,
        logging.ERROR: FAIL + format + ENDC,
        logging.CRITICAL: FAIL + UNDERLINE + format + ENDC,
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

if __name__ == '__main__':
    executor.start_polling(dp)
