# Модель удаления Юзера из базы данных

import requests

from import_buffer import dp
from config import PARSE_USER_LIST_URL, DELETE_USER_URL

from data_base import json_parse_users

from keyboards.client_keyboards import ikb_start, ikb_help, ikb_my_party1, ikb_delete_user_yes_no
from loguru import logger


@dp.callback_query_handler(lambda query: query.data == "ibtn_delete_user", state='*')
async def delete_user(message):
    """Функция удаления Юзера"""

    await message.bot.send_message(message.from_user.id, 'Вы собираетесь удалить свой профиль\n'
                                                         'Для удаления нажмите - <b>"Да"</b>\n'
                                                         'Отменить - <b>"Нет"</b>', reply_markup=ikb_delete_user_yes_no)


@dp.callback_query_handler(lambda query: query.data == "ibtn_delete_user_yes")
async def delete_user_yes(message):
    """Функция подтверждения на удаление Юзера"""
    data = json_parse_users.get_json(url=PARSE_USER_LIST_URL)
    is_user_found = False
    my_item = ""
    for item in data:
        if str(item.get('user_id')) == "@"+str(message.from_user.username):
            is_user_found = True
            my_item = item
    if is_user_found:
        pk = my_item.get('pk')
        requests.delete(url=DELETE_USER_URL+f'{pk}'"")
        logger.info(f"{my_item.get('user_id')} удалил профиль")

    await message.bot.send_message(message.from_user.id, '<b>Ваш профиль удален</b>', reply_markup=ikb_start)


@dp.callback_query_handler(lambda query: query.data == "ibtn_delete_user_no")
async def delete_user_no(message):
    """Функция отказа от удаления Юзера"""

    await message.bot.send_message(message.from_user.id, '<b>Я рад что ты решил остаться с нами!</b>', reply_markup=ikb_help)




