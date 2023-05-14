# Модуль отображения Пати созданой Юзером

from import_buffer import dp
from config import PARSE_PARTY_LIST_URL

from data_base import json_parse_partys
from handlers import i_in_other_party
from keyboards.client_keyboards import ikb_help, ikb_my_party1, ikb_my_party2, ikb_start

from utils import buffer_def


@dp.callback_query_handler(lambda query: query.data == "ibtn_my_party", state='*')
async def my_party(message):
    """Функция отображения Пати созданой Юзером, включает в себя модуль i_in_other_party"""
    is_user_exists = await buffer_def.check_auth(message)
    if is_user_exists:
        data = json_parse_partys.get_json(url=PARSE_PARTY_LIST_URL)
        result = data.get("results")
        is_party_found = False
        item = ""
        my_partys_list = []
        for r in result:
            if str(r.get('leader_id')) == "@"+str(message.from_user.username):
                is_party_found = True
                item = r
            users = r.get('users')
            if users:
                for u in users:
                    my_users_id = u.get('user_id')
                    if my_users_id == "@"+str(message.from_user.username):
                        my_partys_list.append(r)
        if is_party_found:
            await message.bot.send_message(message.from_user.id, '<b>Ваша Пати:</b>')

            my_users = await buffer_def.users(item)

            if my_users == "":
                my_users = str("<b>В Вашей группе нет пользователей</b>")

            cart = await buffer_def.cart(item, my_users)

            await message.bot.send_message(message.from_user.id, cart, reply_markup=ikb_my_party1)

            await i_in_other_party.i_in_other_party(message)
        else:
            await message.bot.send_message(message.from_user.id, '<b>У вас нет пати</b>', reply_markup=ikb_help)
    else:
        await message.bot.send_message(message.from_user.id,
                                   '<b>ОШИБКА! Не создан профиль! Для просмотра вашего пати нужно иметь профиль</b>',
                                   reply_markup=ikb_start)



