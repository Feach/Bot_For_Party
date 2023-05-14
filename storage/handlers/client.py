# Модуль клиентских хендлеров
from aiogram import types, Dispatcher
from config import admin_inside_id, PARSE_USER_LIST_URL
from loguru import logger
from text_base.texts import FIRST_TEXT, HELP_COMMAND
from keyboards import client_keyboards
from keyboards.client_keyboards import ikb_help

from data_base import json_parse_users

from utils import buffer_def


def register_handlers_client(dp: Dispatcher):
    """Функция регистрации клиентких хендлеров"""

    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])


async def start(message: types.Message):
    """Функция клиенткого хендлера при старте"""
    is_user_exists = await buffer_def.check_auth(message)
    if is_user_exists:
        await message.delete()
        await message.bot.send_message(admin_inside_id, 'С возвращением!', reply_markup=ikb_help)
    else:
        await message.bot.send_message(message.from_user.id, text=FIRST_TEXT, reply_markup=client_keyboards.ikb_start)
        await message.delete()
        logger.info(f"@{message.from_user.username} зашел в бота")
        await message.bot.send_message(admin_inside_id, f"В бота зашел @{message.from_user.username}")


async def help(message: types.Message):
    """Функция клиенткого хендлера при help запросе"""

    await message.answer(text=HELP_COMMAND, reply_markup=ikb_help)
    await message.delete()







