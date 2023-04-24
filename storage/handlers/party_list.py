import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from import_buffer import dp

from data_base import json_parse_partys

from keyboards.client_keyboards import ikb_help


class FSMFilter_party(StatesGroup):
    city = State()


@dp.callback_query_handler(lambda query: query.data == "ibtn_party_list")
async def load_city(message: types.Message):
    await FSMFilter_party.city.set()
    await message.bot.send_message(message.from_user.id, 'Введите город:')

    @dp.message_handler(state=FSMFilter_party.city)
    async def first_party_list(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['city'] = message.text
        await FSMFilter_party.next()
        valid_city = json_parse_partys.get_json(url=f"http://127.0.0.1:8000/party_list/?format=json&page_size=1000")
        valid_city_result = valid_city.get("results")
        for item in valid_city_result:
            if item.get('city') == data['city']:

                requests.get(url=f"http://127.0.0.1:8000/party_list/{data['city']}/?format=json&page=1")

                party_list = json_parse_partys.get_json(url=f"http://127.0.0.1:8000/party_list/{data['city']}/?format=json&page=1")

                party_list_result = party_list.get("results")

                counter = 0

                # блок формирования сообщения
                for item in party_list_result:
                    counter += 1
                    users = item.get('users')
                    my_users = ""
                    for user in users:
                        my_user = f"-----------\n{'Имя: '} {user.get('name')}\n" \
                                  f"{'Пол: '} {user.get('gender')}\n" \
                                  f"{'Возраст: '} {user.get('age')}\n" \
                                  f"{'Описание: '} {user.get('discription')}\n" \
                                  f"{'ID: '} {user.get('user_id')}\n"
                        my_users = my_users + my_user

                    cart = f"{'Номер группы: '} {item.get('pk')}\n" \
                           f"{'Тема: '} {item.get('title')}\n" \
                           f"{'Город: '} {item.get('city')}\n" \
                           f"{'Локация: '} {item.get('location')}\n" \
                           f"{'Средний возраст: '} {item.get('age')}\n" \
                           f"{'Описание: '} {item.get('discription')}\n" \
                           f"{'Кол-во пользователей: '} {item.get('user_count')} | {item.get('user_max')}\n" \
                           f"{'Лидер: '} {item.get('leader_id')}\n" \
                           f"{'Пользователи: '} \n " \
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


                    @dp.callback_query_handler(lambda query: query.data == "next_page")
                    async def party_list_next_page(message: types.Message):
                        page_text = message["message"]["reply_markup"]["inline_keyboard"][1]
                        for item in page_text:
                            if item["callback_data"] == "next_page":
                                page_number = item["text"]
                        page_number = page_number.replace("Страница", "").replace(" ", "")
                        next_page = int(page_number)+1
                        previous_page = int(page_number)-1 if int(page_number) > 2 else 1

                        url = f"http://127.0.0.1:8000/party_list/{data['city']}?format=json&page="+page_number
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
                                my_user = f"-----------\n{'Имя: '} {user.get('name')}\n" \
                                          f"{'Пол: '} {user.get('gender')}\n" \
                                          f"{'Возраст: '} {user.get('age')}\n" \
                                          f"{'Описание: '} {user.get('discription')}\n" \
                                          f"{'ID: '} {user.get('user_id')}\n"
                                my_users = my_users + my_user

                            cart = f"{'Номер группы: '} {item.get('pk')}\n" \
                                   f"{'Тема: '} {item.get('title')}\n" \
                                   f"{'Город: '} {item.get('city')}\n" \
                                   f"{'Локация: '} {item.get('location')}\n" \
                                   f"{'Средний возраст: '} {item.get('age')}\n" \
                                   f"{'Описание: '} {item.get('discription')}\n" \
                                   f"{'Кол-во пользователей: '} {item.get('user_count')} | {item.get('user_max')}\n" \
                                   f"{'Лидер: '} {item.get('leader_id')}\n" \
                                   f"{'Пользователи: '} \n " \
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


                    @dp.callback_query_handler(lambda query: query.data == "previous_page")
                    async def party_list_previous_page(message: types.Message):
                        page_text = message["message"]["reply_markup"]["inline_keyboard"][1]
                        for item in page_text:
                            if item["callback_data"] == "previous_page":
                                page_number = item["text"]
                        page_number = page_number.replace("Страница", "").replace(" ", "")
                        next_page = int(page_number) + 1
                        previous_page = int(page_number) - 1 if int(page_number) > 2 else 1

                        url = f"http://127.0.0.1:8000/party_list/{data['city']}?format=json&page=" + page_number
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
                                my_user = f"-----------\n{'Имя: '} {user.get('name')}\n" \
                                          f"{'Пол: '} {user.get('gender')}\n" \
                                          f"{'Возраст: '} {user.get('age')}\n" \
                                          f"{'Описание: '} {user.get('discription')}\n" \
                                          f"{'ID: '} {user.get('user_id')}\n"
                                my_users = my_users + my_user

                            cart = f"{'Номер группы: '} {item.get('pk')}\n" \
                                   f"{'Тема: '} {item.get('title')}\n" \
                                   f"{'Город: '} {item.get('city')}\n" \
                                   f"{'Локация: '} {item.get('location')}\n" \
                                   f"{'Средний возраст: '} {item.get('age')}\n" \
                                   f"{'Описание: '} {item.get('discription')}\n" \
                                   f"{'Кол-во пользователей: '} {item.get('user_count')} | {item.get('user_max')}\n" \
                                   f"{'Лидер: '} {item.get('leader_id')}\n" \
                                   f"{'Пользователи: '} \n " \
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
            else:
                await message.bot.send_message(message.from_user.id, "Из данного города еще нет созданных Пати", reply_markup=ikb_help)
                break


