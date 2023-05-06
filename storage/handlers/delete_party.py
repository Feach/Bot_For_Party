from data_base import json_parse_partys
import requests

from import_buffer import dp

from keyboards.client_keyboards import ikb_delete_party

from config import PARSE_PARTY_LIST_URL, DELETE_PARTY_URL


@dp.callback_query_handler(lambda query: query.data == "ibtn_delete_party")
async def delete_party(message):
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
    await message.bot.send_message(message.from_user.id, 'Ваша пати удалена', reply_markup=ikb_delete_party)



