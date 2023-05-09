# Модуль запуска бота
from aiogram.utils import executor

from import_buffer import dp
from handlers.client import register_handlers_client
from data_base import users_db, party_db

register_handlers_client(dp)


async def on_startup(_):
    """Функция запуска бота и уведомление о подключении к таблицам баз данных"""
    print('Бот работает')
    users_db.sql_users_start()
    party_db.sql_party_start()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

