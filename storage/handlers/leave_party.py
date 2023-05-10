# Модуль выхода из пати
import requests

from import_buffer import dp
from config import DELETE_FROM_PARTY


@dp.callback_query_handler(lambda query: query.data == "ibtn_leave_party", state='*')
async def leave_party(group_id):
    """Функция выхода юзера из пати"""
    text = group_id["message"]["reply_markup"]["inline_keyboard"][2][0]["text"]
    party_pk = text.replace("Выйти из пати №", "")
    user_id = group_id["message"]["chat"]["username"]
    json_data = {
        "party_pk": party_pk,
        "user_id": "@" + user_id
    }

    requests.delete(url=DELETE_FROM_PARTY, json=json_data)




