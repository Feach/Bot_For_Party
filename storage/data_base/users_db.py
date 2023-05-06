# файл функций бд юзеров
import sqlite3
import json

import requests

from data_base import json_parse_users

from keyboards.client_keyboards import ikb_profile

from config import CREATE_USER_URL, UPDATE_PROFILE


# подключение бд к боту
def sql_users_start():
    connection = sqlite3.connect('storage/db.sqlite3')
    cursor = connection.cursor()
    if connection:
        print('storage/db.sqlite3 (users) подключено успешно!')


# Создание юзера из FSM(handlers/create_user.py). Получает state и преобразует его в json.
# После постит на ссылку, от куда его обрабатывает database/views.py(CreateUserView) и создает юзера в бд
async def sql_create_user(state):
    async with state.proxy() as data:
        json_data = {
            "name": data['nikname'],
            "gender": data['gender'],
            "age": data['age'],
            "discription": data['discription'],
            "user_id": data['user_id'],
            "inside_id": data['inside_id']
        }
    requests.post(url=CREATE_USER_URL, json=json_data)


async def sql_update_profile(state):
    async with state.proxy() as data:
        json_data = {
            "name": data['nikname'],
            "gender": data['gender'],
            "age": data['age'],
            "discription": data['discription'],
            "user_id": data['user_id']
        }
    requests.post(url=UPDATE_PROFILE, json=json_data)

