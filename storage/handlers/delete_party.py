# Модель удаления Пати из базы данных
import requests

from import_buffer import dp
from config import PARSE_PARTY_LIST_URL, DELETE_PARTY_URL, STATISTIC_PARTY_DELETE_URL

from data_base import json_parse_partys
from keyboards.client_keyboards import ikb_delete_party, ikb_delete_party_yes_no, ikb_help


@dp.callback_query_handler(lambda query: query.data == "ibtn_delete_party", state='*')
async def delete_party(message):
    """Функция удаления Пати"""
    await message.bot.send_message(message.from_user.id, '<b>Вы собираетесь удалить свой профиль</b>\n'
                                                         'Для удаления нажмите - "Да"\n'
                                                         'Отменить - <b>"Нет"</b>', reply_markup=ikb_delete_party_yes_no)


@dp.callback_query_handler(lambda query: query.data == "ibtn_delete_party_yes")
async def delete_party_yes(message):
    """Функция подтверждения на удаление Пати"""

    data = json_parse_partys.get_json(url=PARSE_PARTY_LIST_URL)
    result = data.get("results")
    is_party_found = False
    my_item = ""
    for item in result:
        if str(item.get('leader_id')) == "@"+str(message.from_user.username):
            is_party_found = True
            my_item = item
    if is_party_found:
        pk = my_item.get('pk')
        requests.delete(url=DELETE_PARTY_URL+f'{pk}'"")
        json_data = {
            "title": my_item.get('title'),
            "category": my_item.get('category'),
            "city": my_item.get('city'),
            "location": my_item.get('location'),
            "age": my_item.get('age'),
            "discription": my_item.get('discription'),
            "default_users": 1,
            "max_users": my_item.get('user_max'),
            "leader_id": my_item.get('leader_id'),
        }
        requests.post(url=STATISTIC_PARTY_DELETE_URL, json=json_data)
    await message.bot.send_message(message.from_user.id, '<b>Ваша пати удалена</b>', reply_markup=ikb_help)


@dp.callback_query_handler(lambda query: query.data == "ibtn_delete_party_no")
async def delete_party_no(message):
    """Функция отказа от удаления Пати"""

    await message.bot.send_message(message.from_user.id, '<b>Удаление пати Отменено</b>', reply_markup=ikb_help)



