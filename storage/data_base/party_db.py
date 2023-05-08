# файл функций бд пати
import json
import math
import sqlite3

import requests
from data_base import json_parse_users, json_parse_partys

from import_buffer import dp

from keyboards.client_keyboards import ikb_connect_to_party, ikb_pagination, main_menu, ikb_my_party1

from config import CREATE_PARTY_URL, PARSE_PARTY_LIST_URL, PARSE_USER_LIST_URL, CONNECT_TO_PARTY_URL, STATISTIC_PARTY_CREATE_URL

# подключение бд к боту
def sql_party_start():
    connection = sqlite3.connect('storage/db.sqlite3')
    cursor = connection.cursor()
    if connection:
        print('storage/db.sqlite3 (party) подключено успешно!')


# Создание пати из FSM(handlers/create_party.py). Получает state и преобразует его в json.
# После постит на ссылку, от куда его обрабатывает database/views.py(CreatePartyView) и создает пати в бд
async def sql_create_party(state):
    async with state.proxy() as data:
        json_data = {
            "title": data['title'],
            "city": data['city'],
            "location": data['location'],
            "age": data['age'],
            "discription": data['discription'],
            "default_users": data['default_users'],
            "max_users": data['max_users'],
            "leader_id": data['leader_id'],
        }
    requests.post(url=CREATE_PARTY_URL, json=json_data)
    requests.post(url=STATISTIC_PARTY_CREATE_URL, json=json_data)


@dp.callback_query_handler(lambda query: query.data == "connect_to_data")
async def sql_connect_to_party(message):
    text = message["message"]["reply_markup"]["inline_keyboard"][0][0]["text"]
    party_pk = text.replace("Подключиться к группе №", "")
    user_id = message["message"]["chat"]["username"]
    party_data = json_parse_partys.get_json(url=PARSE_PARTY_LIST_URL)
    user_data = json_parse_users.get_json(url=PARSE_USER_LIST_URL)
    party_data_result = party_data.get("results")
    for item in party_data_result:
        if int(item.get('pk')) == int(party_pk):
            if int(item.get('user_max')) >= int(item.get('user_count')) + 1:
                json_data = {
                "party_pk": party_pk,
                "user_id": "@"+user_id
            }
                await message.bot.send_message(message.from_user.id, f'Вы подключились к пати №{party_pk}')

                requests.post(url=CONNECT_TO_PARTY_URL, json=json_data)

                for party_item in party_data_result:
                    if int(party_item.get('pk')) == int(party_pk):
                        for user_item in user_data:
                            if party_item.get('leader_id') == user_item.get('user_id'):
                                leader_inside_id = user_item.get('inside_id')
                                connect_user_id = "@"+message.from_user.username
                                await message.bot.send_message(leader_inside_id, f'К вашей пати №{party_pk} подключился {connect_user_id}')
            else:
                await message.bot.send_message(message.from_user.id, f'Ошибка присоединения к пати №{party_pk}! (Достигнут лимит пользователей)')















