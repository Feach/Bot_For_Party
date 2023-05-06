# файл в котором указываются экземпляры бота
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

storage = MemoryStorage()

bot = Bot(config.API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

