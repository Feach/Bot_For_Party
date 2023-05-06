import json
import math
import sqlite3

import requests
from aiogram import types
from data_base import json_parse_partys

from import_buffer import dp

from keyboards.client_keyboards import ikb_connect_to_party, ikb_pagination, main_menu, ikb_my_party1

from config import DELETE_FROM_PARTY


@dp.callback_query_handler(lambda query: query.data == "ibtn_leave_party")
async def leave_party(group_id):
    text = group_id["message"]["reply_markup"]["inline_keyboard"][2][0]["text"]
    party_pk = text.replace("Выйти из пати №", "")
    user_id = group_id["message"]["chat"]["username"]
    json_data = {
        "party_pk": party_pk,
        "user_id": "@" + user_id
    }
    print(json_data)

    requests.delete(url=DELETE_FROM_PARTY, json=json_data)




