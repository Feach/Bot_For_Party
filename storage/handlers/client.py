# файл со всеми функциями которыми пользуются юзеры
from aiogram import types, Dispatcher
from text_base.texts import first_text
from keyboards import client_keyboards
from keyboards.client_keyboards import ikb_help

# буферы тескта
HELP_COMMAND = """
/help - Команды бота

Ниже все кнопки для управления ботом
"""

FIRST_TEXT = first_text


# регистрация хендлеров
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(text=first_text, reply_markup=client_keyboards.ikb_start)
    await message.delete()


# @dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(text=HELP_COMMAND, reply_markup=ikb_help)
    await message.delete()


# @dp.message_handler()
# async def cenz_mat(message: types.Message):
#     if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
#             .intersection(set(json.load(open('cenz.json')))) != set():
#         await message.reply('Маты запрещены')
#         await message.delete()








