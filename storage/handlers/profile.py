# Модуль отображения информации о юзере
from import_buffer import dp
from config import PARSE_USER_LIST_URL

from data_base import json_parse_users

from keyboards.client_keyboards import ikb_profile, ikb_start


@dp.callback_query_handler(lambda query: query.data == "ibtn_profile")
async def profile(message):
    """Функция отображения информации о юзере"""
    data = json_parse_users.get_json(url=PARSE_USER_LIST_URL)
    is_user_found = False
    my_item = ""
    for item in data:
        if str(item.get('user_id')) == "@"+str(message.from_user.username):
            is_user_found = True
            my_item = item
    if is_user_found:
        await message.bot.send_message(message.from_user.id, '<b>Ваш профиль:</b>')

        cart = f"{'<b>Имя: </b>'} {my_item.get('name')}\n" \
               f"{'<b>Пол: </b>'} {my_item.get('gender')}\n" \
               f"{'<b>Возраст: </b>'} {my_item.get('age')}\n" \
               f"{'<b>Описание: </b>'} {my_item.get('discription')}\n" \
               f"{'<b>ID: </b>'} {my_item.get('user_id')}\n"
        await message.bot.send_message(message.from_user.id, cart, reply_markup=ikb_profile)
    else:
        await message.bot.send_message(message.from_user.id, 'У вас нет профиля. \nДля создания своего профиля нажмите на кнопку 👇', reply_markup=ikb_start)
