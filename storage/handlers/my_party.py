from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base import json_parse_partys

from import_buffer import dp

from keyboards.client_keyboards import ikb_help, ikb_my_party1, ikb_my_party2

from config import PARSE_PARTY_LIST_URL


@dp.callback_query_handler(lambda query: query.data == "ibtn_my_party")
async def my_party(message):
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
               f"{'<b>Локация: </b>'} {my_item.get('location')}\n" \
               f"{'<b>Средний возраст: </b>'} {my_item.get('age')}\n" \
               f"{'<b>Описание: </b>'} {my_item.get('discription')}\n" \
               f"{'<b>Кол-во пользователей: </b>'} {my_item.get('user_count')} | {my_item.get('user_max')}\n" \
               f"{'<b>Лидер: </b>'} {my_item.get('leader_id')}\n" \
               f"{'<b>Пользователи: </b>'} \n " \
               f"{my_users}\n "
        await message.bot.send_message(message.from_user.id, cart, reply_markup=ikb_my_party1)
        await message.bot.send_message(message.from_user.id, "<b>===================================</b>")

    if my_partys_list:
        await message.bot.send_message(message.from_user.id, '<b>Вы находить в пати:</b>')
        for party in my_partys_list:
            users = party.get('users')
            my_users = ""
            for user in users:
                my_user = f"-----------\n{'<b>Имя: </b>'} {user.get('name')}\n" \
                          f"{'<b>Пол: </b>'} {user.get('gender')}\n" \
                          f"{'<b>Возраст: </b>'} {user.get('age')}\n" \
                          f"{'<b>Описание: </b>'} {user.get('discription')}\n" \
                          f"{'<b>ID: </b>'} {user.get('user_id')}\n"
                my_users = my_users + my_user
            if my_users == "":
                my_users = str("<b>В Вашей группе нет пользователей</b>")

            cart = f"{'<b>Номер группы: </b>'} {party.get('pk')}\n" \
                   f"{'<b>Тема: </b>'} {party.get('title')}\n" \
                   f"{'<b>Локация: </b>'} {party.get('location')}\n" \
                   f"{'<b>Средний возраст: </b>'} {party.get('age')}\n" \
                   f"{'<b>Описание: </b>'} {party.get('discription')}\n" \
                   f"{'<b>Кол-во пользователей: </b>'} {party.get('user_count')} <b>|</b> {party.get('user_max')}\n" \
                   f"{'<b>Лидер: </b>'} {party.get('leader_id')}\n" \
                   f"{'<b>Пользователи: </b>'} \n " \
                   f"{my_users}\n "

            ibtn_leave_party = InlineKeyboardMarkup()
            ibtn_leave_party.row_width = 2

            ibtn_leave_party.add(
                InlineKeyboardButton('Профиль', callback_data='ibtn_profile')
            )

            ibtn_leave_party.row(
                InlineKeyboardButton('Создать Пати', callback_data='ibtn_create_party'),
                InlineKeyboardButton('Список Пати', callback_data='ibtn_party_list')
            )

            ibtn_leave_party.add(
                InlineKeyboardButton(f"{'Выйти из пати №'}{party.get('pk')}", group_id=party.get('pk'),
                                     callback_data="ibtn_leave_party")
            )

            await message.bot.send_message(message.from_user.id, cart, reply_markup=ibtn_leave_party)

    else:
        await message.bot.send_message(message.from_user.id, '<b>У вас еще нет своей пати и вы не состоите ни в какой пати</b>', reply_markup=ikb_my_party1)



