# Модуль с функциями для работы с sql и DRF
import sqlite3
import requests

from config import CREATE_USER_URL, UPDATE_PROFILE_URL


def sql_users_start():
    """Функция запуска бд таблицы (users)"""
    connection = sqlite3.connect('storage/db.sqlite3')
    cursor = connection.cursor()
    if connection:
        print('storage/db.sqlite3 (users) подключено успешно!')


async def sql_create_user(state):
    """Функция отправки post запроса для создания User"""
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
    """Функция отправки post запроса для обновления данных User"""

    async with state.proxy() as data:
        json_data = {
            "name": data['nikname'],
            "gender": data['gender'],
            "age": data['age'],
            "discription": data['discription'],
            "user_id": data['user_id']
        }
    requests.post(url=UPDATE_PROFILE_URL, json=json_data)

