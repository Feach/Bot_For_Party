import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from import_buffer import dp

from data_base import json_parse_partys

from keyboards.client_keyboards import ikb_help

from config import PARSE_PARTY_LIST_URL, MAIN_PARTY_LIST_URL


class FSMFilter_party(StatesGroup):
    category = State()
    city = State()
    url = State()


@dp.callback_query_handler(lambda query: query.data == "ibtn_party_list")
async def start_party_list(message: types.Message):
    await FSMFilter_party.category.set()
    await message.bot.send_message(message.from_user.id, '<b>Введите категорию\nНажмите "Далее" что пропустить</b>')

    @dp.message_handler(state=FSMFilter_party.category)
    async def load_category(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['category'] = message.text
            await FSMFilter_party.next()
            await message.bot.send_message(message.from_user.id, '<b>Введите название городе:</b>')

    @dp.message_handler(state=FSMFilter_party.city)
    async def load_city(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['city'] = message.text
            await FSMFilter_party.next()
            if data['category'] == "Далее":
                url_with_only_city = MAIN_PARTY_LIST_URL + f"{data['city']}/" + "?format=json&page="
                full_url_with_only_city = url_with_only_city + str(1)
                data['url'] = url_with_only_city

                valid_city = json_parse_partys.get_json(url=full_url_with_only_city)
                valid_city_result = valid_city.get("results")
                counter = 0

                party_exists = False
                for item in valid_city_result:
                    if data['city'] == item.get('city'):
                        party_exists = True
                        counter += 1
                    if party_exists:
                        users = item.get('users')
                        my_users = ""
                        for user in users:
                            my_user = f"<b>-----------</b>\n{'<b>Имя: </b>'} {user.get('name')}\n" \
                                      f"{'<b>Пол: </b>'} {user.get('gender')}\n" \
                                      f"{'<b>Возраст: </b>'} {user.get('age')}\n" \
                                      f"{'<b>Описание: </b>'} {user.get('discription')}\n" \
                                      f"{'<b>ID: </b>'} {user.get('user_id')}\n"
                            my_users = my_users + my_user

                        cart = f"{'<b>Номер группы: </b>'} {item.get('pk')}\n" \
                               f"{'<b>Тема: </b>'} {item.get('title')}\n" \
                               f"{'<b>Категория: </b>'} {item.get('category')}\n" \
                               f"{'<b>Город: </b>'} {item.get('city')}\n" \
                               f"{'<b>Локация: </b>'} {item.get('location')}\n" \
                               f"{'<b>Средний возраст: </b>'} {item.get('age')}\n" \
                               f"{'<b>Описание: </b>'} {item.get('discription')}\n" \
                               f"{'<b>Кол-во пользователей: </b>'} {item.get('user_count')} <b>|</b> {item.get('user_max')}\n" \
                               f"{'<b>Лидер: </b>'} {item.get('leader_id')}\n" \
                               f"{'<b>Пользователи: </b>'} \n " \
                               f"{my_users}\n "

                        ibt_connect_to_party = InlineKeyboardMarkup()
                        ibt_connect_to_party.row_width = 2
                        if counter < 1:
                            if int(item.get('user_max')) >= int(item.get('user_count')) + 1:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton(f"{'Подключиться к группе №'}{item.get('pk')}", group_id=item.get('pk'),
                                                         callback_data="connect_to_data"))
                            else:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton("Достигнут лимит подключений", callback_data="limit"))
                        else:
                            if int(item.get('user_max')) >= int(item.get('user_count')) + 1:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton(f"{'Подключиться к группе №'}{item.get('pk')}", group_id=item.get('pk'),
                                                         callback_data="connect_to_data"))
                            else:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton("Достигнут лимит подключений", callback_data="limit"))
                                ibt_connect_to_party.row(
                                    InlineKeyboardButton("Страница 2", callback_data="next_page")
                                )
                        await message.bot.send_message(message.from_user.id, cart, reply_markup=ibt_connect_to_party)

                        if counter == 4:
                            break

                if party_exists is False:
                    await message.bot.send_message(message.from_user.id, "<b>В данном городе еще нет пати</b>\n"
                                                                         "<b>Проверьте название города или создайте пати</b>",
                                                   reply_markup=ikb_help)

            else:
                url_with_category_and_city = MAIN_PARTY_LIST_URL + f"{data['category']}/"+f"{data['city']}/" + "?format=json&page="
                data['url'] = url_with_category_and_city
                full_url_with_category_and_city = url_with_category_and_city + str(1)

                valid_city = json_parse_partys.get_json(url=full_url_with_category_and_city)
                valid_city_result = valid_city.get("results")
                counter = 0

                party_exists = False
                for item in valid_city_result:
                    if data['city'] == item.get('city'):
                        party_exists = True
                        counter += 1
                    if party_exists:
                        users = item.get('users')
                        my_users = ""
                        for user in users:
                            my_user = f"<b>-----------</b>\n{'<b>Имя: </b>'} {user.get('name')}\n" \
                                      f"{'<b>Пол: </b>'} {user.get('gender')}\n" \
                                      f"{'<b>Возраст: </b>'} {user.get('age')}\n" \
                                      f"{'<b>Описание: </b>'} {user.get('discription')}\n" \
                                      f"{'<b>ID: </b>'} {user.get('user_id')}\n"
                            my_users = my_users + my_user

                        cart = f"{'<b>Номер группы: </b>'} {item.get('pk')}\n" \
                               f"{'<b>Тема: </b>'} {item.get('title')}\n" \
                               f"{'<b>Категория: </b>'} {item.get('category')}\n" \
                               f"{'<b>Город: </b>'} {item.get('city')}\n" \
                               f"{'<b>Локация: </b>'} {item.get('location')}\n" \
                               f"{'<b>Средний возраст: </b>'} {item.get('age')}\n" \
                               f"{'<b>Описание: </b>'} {item.get('discription')}\n" \
                               f"{'<b>Кол-во пользователей: </b>'} {item.get('user_count')} <b>|</b> {item.get('user_max')}\n" \
                               f"{'<b>Лидер: </b>'} {item.get('leader_id')}\n" \
                               f"{'<b>Пользователи: </b>'} \n " \
                               f"{my_users}\n "

                        ibt_connect_to_party = InlineKeyboardMarkup()
                        ibt_connect_to_party.row_width = 2
                        if counter < 4:
                            if int(item.get('user_max')) >= int(item.get('user_count')) + 1:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton(f"{'Подключиться к группе №'}{item.get('pk')}", group_id=item.get('pk'),
                                                         callback_data="connect_to_data"))
                            else:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton("Достигнут лимит подключений", callback_data="limit"))
                        else:
                            if int(item.get('user_max')) >= int(item.get('user_count')) + 1:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton(f"{'Подключиться к группе №'}{item.get('pk')}", group_id=item.get('pk'),
                                                         callback_data="connect_to_data"))
                            else:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton("Достигнут лимит подключений", callback_data="limit"))
                                ibt_connect_to_party.row(
                                    InlineKeyboardButton("Страница 2", callback_data="next_page")
                                )
                        await message.bot.send_message(message.from_user.id, cart, reply_markup=ibt_connect_to_party)

                        if counter == 4:
                            break

                if party_exists is False:
                    await message.bot.send_message(message.from_user.id, "<b>В данном городе еще нет пати</b>\n"
                                                                         "<b>Проверьте название города или создайте пати</b>",
                                                   reply_markup=ikb_help)

                @dp.callback_query_handler(lambda query: query.data == "next_page")
                async def party_list_next_page(message: types.Message):
                    page_text = message["message"]["reply_markup"]["inline_keyboard"][1]
                    for item in page_text:
                        if item["callback_data"] == "next_page":
                            page_number = item["text"]
                    page_number = page_number.replace("Страница", "").replace(" ", "")
                    next_page = int(page_number) + 1
                    previous_page = int(page_number) - 1 if int(page_number) > 2 else 1

                    url = data['url'] + page_number
                    party_list = json_parse_partys.get_json(url=url)
                    party_list_result = party_list.get("results")
                    next_page_true = party_list.get("next")

                    counter = 0

                    # блок формирования сообщения
                    for item in party_list_result:
                        counter += 1
                        users = item.get('users')
                        my_users = ""
                        for user in users:
                            my_user = f"<b>-----------</b>\n{'<b>Имя: </b>'} {user.get('name')}\n" \
                                      f"{'<b>Пол: </b>'} {user.get('gender')}\n" \
                                      f"{'<b>Возраст: </b>'} {user.get('age')}\n" \
                                      f"{'<b>Описание: </b>'} {user.get('discription')}\n" \
                                      f"{'<b>ID: </b>'} {user.get('user_id')}\n"
                            my_users = my_users + my_user

                        cart = f"{'<b>Номер группы: </b>'} {item.get('pk')}\n" \
                               f"{'<b>Тема: </b>'} {item.get('title')}\n" \
                               f"{'<b>Категория: </b>'} {item.get('category')}\n" \
                               f"{'<b>Город: </b>'} {item.get('city')}\n" \
                               f"{'<b>Локация: </b>'} {item.get('location')}\n" \
                               f"{'<b>Средний возраст: </b>'} {item.get('age')}\n" \
                               f"{'<b>Описание: </b>'} {item.get('discription')}\n" \
                               f"{'<b>Кол-во пользователей: </b>'} {item.get('user_count')} <b>|</b> {item.get('user_max')}\n" \
                               f"{'<b>Лидер: </b>'} {item.get('leader_id')}\n" \
                               f"{'<b>Пользователи: </b>'} \n " \
                               f"{my_users}\n "

                        ibt_connect_to_party = InlineKeyboardMarkup()
                        ibt_connect_to_party.row_width = 2
                        if counter < 4:
                            if int(item.get('user_max')) >= int(item.get('user_count')) + 1:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton(f"{'Подключиться к группе №'}{item.get('pk')}",
                                                         group_id=item.get('pk'),
                                                         callback_data="connect_to_data"))
                            else:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton("Достигнут лимит подключений", callback_data="limit"))
                        else:
                            if int(item.get('user_max')) >= int(item.get('user_count')) + 1:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton(f"{'Подключиться к группе №'}{item.get('pk')}",
                                                         group_id=item.get('pk'),
                                                         callback_data="connect_to_data"))
                            else:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton("Достигнут лимит подключений", callback_data="limit"))
                            if next_page_true is None:
                                ibt_connect_to_party.row(
                                    InlineKeyboardButton(f"{'Страница'} {previous_page}", callback_data="previous_page"),
                                )
                            else:
                                ibt_connect_to_party.row(
                                    InlineKeyboardButton(f"{'Страница'} {previous_page}", callback_data="previous_page"),
                                    InlineKeyboardButton(f"{'Страница'} {next_page}", callback_data="next_page")
                                )
                        await message.bot.send_message(message.from_user.id, cart, reply_markup=ibt_connect_to_party)

                        if counter == 4:
                            break

                await FSMFilter_party.next()

                @dp.callback_query_handler(lambda query: query.data == "previous_page")
                async def party_list_previous_page(message: types.Message):
                    page_text = message["message"]["reply_markup"]["inline_keyboard"][1]
                    for item in page_text:
                        if item["callback_data"] == "previous_page":
                            page_number = item["text"]
                    page_number = page_number.replace("Страница", "").replace(" ", "")
                    next_page = int(page_number) + 1
                    previous_page = int(page_number) - 1 if int(page_number) > 2 else 1

                    url = data['url'] + page_number
                    party_list = json_parse_partys.get_json(url=url)
                    party_list_result = party_list.get("results")
                    previous_pagination_page = party_list.get("previous")

                    counter = 0

                    # блок формирования сообщения
                    for item in party_list_result:
                        counter += 1
                        users = item.get('users')
                        my_users = ""
                        for user in users:
                            my_user = f"<b>-----------</b>\n{'<b>Имя: </b>'} {user.get('name')}\n" \
                                      f"{'<b>Пол: </b>'} {user.get('gender')}\n" \
                                      f"{'<b>Возраст: </b>'} {user.get('age')}\n" \
                                      f"{'<b>Описание: </b>'} {user.get('discription')}\n" \
                                      f"{'<b>ID: </b>'} {user.get('user_id')}\n"
                            my_users = my_users + my_user

                        cart = f"{'<b>Номер группы: </b>'} {item.get('pk')}\n" \
                               f"{'<b>Тема: </b>'} {item.get('title')}\n" \
                               f"{'<b>Категория: </b>'} {item.get('category')}\n" \
                               f"{'<b>Город: </b>'} {item.get('city')}\n" \
                               f"{'<b>Локация: </b>'} {item.get('location')}\n" \
                               f"{'<b>Средний возраст: </b>'} {item.get('age')}\n" \
                               f"{'<b>Описание: </b>'} {item.get('discription')}\n" \
                               f"{'<b>Кол-во пользователей: </b>'} {item.get('user_count')} <b>|</b> {item.get('user_max')}\n" \
                               f"{'<b>Лидер: </b>'} {item.get('leader_id')}\n" \
                               f"{'<b>Пользователи: </b>'} \n " \
                               f"{my_users}\n "

                        ibt_connect_to_party = InlineKeyboardMarkup()
                        ibt_connect_to_party.row_width = 2
                        if counter < 4:
                            if int(item.get('user_max')) >= int(item.get('user_count')) + 1:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton(f"{'Подключиться к группе №'}{item.get('pk')}",
                                                         group_id=item.get('pk'),
                                                         callback_data="connect_to_data"))
                            else:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton("Достигнут лимит подключений", callback_data="limit"))
                        else:
                            if int(item.get('user_max')) >= int(item.get('user_count')) + 1:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton(f"{'Подключиться к группе №'}{item.get('pk')}",
                                                         group_id=item.get('pk'),
                                                         callback_data="connect_to_data"))
                            else:
                                ibt_connect_to_party.add(
                                    InlineKeyboardButton("Достигнут лимит подключений", callback_data="limit"))
                            if previous_pagination_page is None:
                                ibt_connect_to_party.row(
                                    InlineKeyboardButton(f"{'Страница'} {next_page}", callback_data="next_page")
                                )
                            else:
                                ibt_connect_to_party.row(
                                    InlineKeyboardButton(f"{'Страница'} {previous_page}", callback_data="previous_page"),
                                    InlineKeyboardButton(f"{'Страница'} {next_page}", callback_data="next_page")
                                )
                        await message.bot.send_message(message.from_user.id, cart, reply_markup=ibt_connect_to_party)

                        if counter == 4:
                            break




