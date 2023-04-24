from data_base import json_parse_partys
import requests

from import_buffer import dp

from keyboards.client_keyboards import ikb_help, ikb_my_party1, ikb_delete_user_yes_no

from data_base import json_parse_users

from keyboards.client_keyboards import ikb_start


@dp.callback_query_handler(lambda query: query.data == "ibtn_delete_user")
async def delete_user(message):
    await message.bot.send_message(message.from_user.id, 'Вы собираетесь удалить свой профиль\n'
                                                         'Для удаления нажмите - "Да"\n'
                                                         'Отменить - "Нет"', reply_markup=ikb_delete_user_yes_no)


@dp.callback_query_handler(lambda query: query.data == "ibtn_delete_user_yes")
async def delete_user_yes(message):
    data = json_parse_users.get_json(url="http://127.0.0.1:8000/users/?format=json&page=1&page_size=1000")
    is_user_found = False
    my_item = ""
    for item in data:
        if str(item.get('user_id')) == "@"+str(message.from_user.username):
            is_user_found = True
            my_item = item
    if is_user_found:
        pk = my_item.get('pk')
        requests.delete(url="http://127.0.0.1:8000/delete_users/"f'{pk}'"")
    await message.bot.send_message(message.from_user.id, 'Ваш профиль удален', reply_markup=ikb_start)


@dp.callback_query_handler(lambda query: query.data == "ibtn_delete_user_no")
async def delete_user_no(message):
    await message.bot.send_message(message.from_user.id, 'Я рад что ты решил остаться с нами!', reply_markup=ikb_help)



