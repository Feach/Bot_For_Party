# Модуль отображения Пати созданой Юзером

from import_buffer import dp
from config import PARSE_PARTY_LIST_URL

from data_base import json_parse_partys
from handlers import i_in_other_party
from keyboards.client_keyboards import ikb_help, ikb_my_party1, ikb_my_party2


@dp.callback_query_handler(lambda query: query.data == "ibtn_my_party")
async def my_party(message):
    """Функция отображения Пати созданой Юзером, включает в себя модуль i_in_other_party"""

    data = json_parse_partys.get_json(url=PARSE_PARTY_LIST_URL)
    result = data.get("results")
    is_party_found = False
    my_item = ""
    my_partys_list = []
    for item in result:
        if str(item.get('leader_id')) == "@"+str(message.from_user.username):
            is_party_found = True
            my_item = item
        users = item.get('users')
        if users:
            for u in users:
                my_users_id = u.get('user_id')
                if my_users_id == "@"+str(message.from_user.username):
                    my_partys_list.append(item)
    if is_party_found:
        await message.bot.send_message(message.from_user.id, '<b>Ваша Пати:</b>')
        users = my_item.get('users')
        my_users = ""
        for user in users:
            my_user = f"<b>-----------</b>\n{'<b>Имя: </b>'} {user.get('name')}\n" \
                      f"{'<b>Пол: </b>'} {user.get('gender')}\n" \
                      f"{'<b>Возраст: </b>'} {user.get('age')}\n" \
                      f"{'<b>Описание: </b>'} {user.get('discription')}\n" \
                      f"{'<b>ID: </b>'} {user.get('user_id')}\n"
            my_users = my_users + my_user
        if my_users == "":
            my_users = str("<b>В Вашей группе нет пользователей</b>")

        cart = f"{'<b>Номер группы: </b>'} {my_item.get('pk')}\n" \
               f"{'<b>Тема: </b>'} {my_item.get('title')}\n" \
               f"{'<b>Категория: </b>'} {my_item.get('category')}\n" \
               f"{'<b>Город: </b>'} {my_item.get('city')}\n" \
               f"{'<b>Локация: </b>'} {my_item.get('location')}\n" \
               f"{'<b>Средний возраст: </b>'} {my_item.get('age')}\n" \
               f"{'<b>Описание: </b>'} {my_item.get('discription')}\n" \
               f"{'<b>Кол-во пользователей: </b>'} {my_item.get('user_count')} | {my_item.get('user_max')}\n" \
               f"{'<b>Лидер: </b>'} {my_item.get('leader_id')}\n" \
               f"{'<b>Пользователи: </b>'} \n " \
               f"{my_users}\n "
        await message.bot.send_message(message.from_user.id, cart, reply_markup=ikb_my_party1)
        await message.bot.send_message(message.from_user.id, "<b>===================================</b>")

        await i_in_other_party.i_in_other_party(message)


