from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base import json_parse_partys

from import_buffer import dp

from keyboards.client_keyboards import ikb_help, ikb_my_party1, ikb_my_party2


@dp.callback_query_handler(lambda query: query.data == "ibtn_my_party")
async def my_party(message):
    data = json_parse_partys.get_json(url="http://127.0.0.1:8000/party_list/?format=json&page_size=1000")
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
        await message.bot.send_message(message.from_user.id, 'Ваша Пати:')
        users = my_item.get('users')
        my_users = ""
        for user in users:
            my_user = f"-----------\n{'Имя: '} {user.get('name')}\n" \
                      f"{'Пол: '} {user.get('gender')}\n" \
                      f"{'Возраст: '} {user.get('age')}\n" \
                      f"{'Описание: '} {user.get('discription')}\n" \
                      f"{'ID: '} {user.get('user_id')}\n"
            my_users = my_users + my_user
        if my_users == "":
            my_users = str("В Вашей группе нет пользователей")

        cart = f"{'Номер группы: '} {my_item.get('pk')}\n" \
               f"{'Тема: '} {my_item.get('title')}\n" \
               f"{'Локация: '} {my_item.get('location')}\n" \
               f"{'Средний возраст: '} {my_item.get('age')}\n" \
               f"{'Описание: '} {my_item.get('discription')}\n" \
               f"{'Кол-во пользователей: '} {my_item.get('user_count')} | {my_item.get('user_max')}\n" \
               f"{'Лидер: '} {my_item.get('leader_id')}\n" \
               f"{'Пользователи: '} \n " \
               f"{my_users}\n "
        await message.bot.send_message(message.from_user.id, cart, reply_markup=ikb_my_party1)
        await message.bot.send_message(message.from_user.id, "===================================")

    if my_partys_list:
        await message.bot.send_message(message.from_user.id, 'Вы находить в пати:')
        for party in my_partys_list:
            users = party.get('users')
            my_users = ""
            for user in users:
                my_user = f"-----------\n{'Имя: '} {user.get('name')}\n" \
                          f"{'Пол: '} {user.get('gender')}\n" \
                          f"{'Возраст: '} {user.get('age')}\n" \
                          f"{'Описание: '} {user.get('discription')}\n" \
                          f"{'ID: '} {user.get('user_id')}\n"
                my_users = my_users + my_user
            if my_users == "":
                my_users = str("В Вашей группе нет пользователей")

            cart = f"{'Номер группы: '} {party.get('pk')}\n" \
                   f"{'Тема: '} {party.get('title')}\n" \
                   f"{'Локация: '} {party.get('location')}\n" \
                   f"{'Средний возраст: '} {party.get('age')}\n" \
                   f"{'Описание: '} {party.get('discription')}\n" \
                   f"{'Кол-во пользователей: '} {party.get('user_count')} | {party.get('user_max')}\n" \
                   f"{'Лидер: '} {party.get('leader_id')}\n" \
                   f"{'Пользователи: '} \n " \
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
        await message.bot.send_message(message.from_user.id, 'У вас еще нет своей пати и вы не состоите ни в какой пати', reply_markup=ikb_my_party1)



