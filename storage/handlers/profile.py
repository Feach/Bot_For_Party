# Получения профиля юзера. С просмотром всей инфы о нем.
from data_base import json_parse_users

from import_buffer import dp

from keyboards.client_keyboards import ikb_profile, ikb_start

from config import PARSE_USER_LIST_URL


@dp.callback_query_handler(lambda query: query.data == "ibtn_profile")
async def profile(message):
    await message.answer("Подождите запрос обрабатывается")
    data = json_parse_users.get_json(url=PARSE_USER_LIST_URL)
    is_user_found = False
    my_item = ""
    for item in data:
        if str(item.get('user_id')) == "@"+str(message.from_user.username):
            is_user_found = True
            my_item = item
    if is_user_found:
        await message.bot.send_message(message.from_user.id, 'Ваш профиль:')

        cart = f"{'Имя: '} {my_item.get('name')}\n" \
               f"{'Пол: '} {my_item.get('gender')}\n" \
               f"{'Возраст: '} {my_item.get('age')}\n" \
               f"{'Описание: '} {my_item.get('discription')}\n" \
               f"{'ID: '} {my_item.get('user_id')}\n"
        await message.bot.send_message(message.from_user.id, cart, reply_markup=ikb_profile)
    else:
        await message.bot.send_message(message.from_user.id, 'У вас нет профиля. Создайте', reply_markup=ikb_start)
