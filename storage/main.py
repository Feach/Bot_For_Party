# файл запуска бота
from aiogram.utils import executor

from import_buffer import dp


# from handlers.create_user import register_handlers_create_user
# from handlers.connect_to_party import register_handlers_connect_to_party
# from handlers.create_party import register_handlers_create_party
from handlers.client import register_handlers_client

from data_base import users_db, party_db

# запуск хендлеров из файлов handlers
register_handlers_client(dp)
# register_handlers_create_user(dp)
# register_handlers_create_party(dp)
# register_handlers_connect_to_party(dp)


async def on_startup(_):
    print('Бот работает')
    users_db.sql_users_start()
    party_db.sql_party_start()


# skip_updates нужна что бы не отвечал после запуска на все пропущенные сообщения
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

