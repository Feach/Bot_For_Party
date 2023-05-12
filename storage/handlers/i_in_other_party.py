# Модуль отображения юзера в других пати, в которых он состоит
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import PARSE_PARTY_LIST_URL

from data_base import json_parse_partys
from keyboards.client_keyboards import ikb_help

from utils import buffer_def


async def i_in_other_party(message):
    """Функция для отображения пользователя в других Пати, в которых он состоит"""
    data = json_parse_partys.get_json(url=PARSE_PARTY_LIST_URL)
    result = data.get("results")
    my_partys_list = []
    for r in result:
        if str(r.get('leader_id')) == "@" + str(message.from_user.username):
            my_item = r
        users = r.get('users')
        if users:
            for u in users:
                my_users_id = u.get('user_id')
                if my_users_id == "@" + str(message.from_user.username):
                    my_partys_list.append(r)
    if my_partys_list:
        await message.bot.send_message(message.from_user.id, '<b>Вы находить в пати:</b>')
        for item in my_partys_list:

            my_users = await buffer_def.users(item)

            if my_users == "":
                my_users = str("<b>В Вашей группе нет пользователей</b>")

            cart = await buffer_def.cart(item, my_users)

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
                InlineKeyboardButton(f"{'Выйти из пати №'}{item.get('pk')}", group_id=item.get('pk'),
                                     callback_data="ibtn_leave_party")
            )

            await message.bot.send_message(message.from_user.id, cart, reply_markup=ibtn_leave_party)

    else:
        await message.bot.send_message(message.from_user.id, '<b>Вы не состоите в чужих пати</b>', reply_markup=ikb_help)


