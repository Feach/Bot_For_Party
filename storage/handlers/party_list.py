# Модуль отображения списка Пати
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from import_buffer import dp
from config import PARSE_PARTY_LIST_URL, MAIN_PARTY_LIST_URL

from data_base import json_parse_partys

from keyboards.client_keyboards import ikb_help, button_category, ikb_start

from utils import buffer_def


class FSMFilter_party(StatesGroup):
    """Класс определения переменных FSM"""
    category = State()
    city = State()
    url = State()


@dp.callback_query_handler(lambda query: query.data == "ibtn_party_list", state='*')
async def start_party_list(message: types.Message):
    """Функция запуска FSM для отображения списка пати"""
    is_user_exists = await buffer_def.check_auth(message)
    if is_user_exists:
        await FSMFilter_party.category.set()
        await message.bot.send_message(message.from_user.id, '<b>Выберете</b> или <b>Введите категорию: \nНажмите "Далее", что бы пропустить.</b>', reply_markup=button_category)

        @dp.message_handler(state=FSMFilter_party.category)
        async def load_category(message: types.Message, state: FSMContext):
            """Функция приема категории для фильтрации """

            async with state.proxy() as data:
                data['category'] = message.text
                data['category'] = data['category'].lower().capitalize()
                await FSMFilter_party.next()
                await message.bot.send_message(message.from_user.id, '<b>Введите название города:</b>', reply_markup=ReplyKeyboardRemove())

        @dp.message_handler(state=FSMFilter_party.city)
        async def load_city(message: types.Message, state: FSMContext):
            """Функция приема категории для фильтрации и дальнейшее выведения списка пати по запросу"""

            async with state.proxy() as data:
                data['city'] = message.text
                data['city'] = data['city'].lower().capitalize()

                await FSMFilter_party.next()
                if data['category'] == "Далее":
                    url_with_only_city = MAIN_PARTY_LIST_URL + f"{data['city']}/" + "?format=json&page="
                    full_url_with_only_city = url_with_only_city + str(1)
                    data['url'] = url_with_only_city

                    parse = json_parse_partys.get_json(url=full_url_with_only_city)
                    parse_result = parse.get("results")
                    counter = 0

                    party_exists = False
                    for item in parse_result:
                        if data['city'] == item.get('city'):
                            party_exists = True
                            counter += 1
                        if party_exists:

                            my_users = await buffer_def.users(item)

                            cart = await buffer_def.cart(item, my_users)
                            if item.get('lat') and item.get('lon') != "-":
                                lat = item.get('lat')
                                lon = item.get('lon')
                                ibt_connect_to_party = await buffer_def.keyboard_party_list(counter, item, parse)

                                await message.bot.send_message(message.from_user.id, cart)
                                await message.bot.send_location(message.from_user.id, latitude=lat, longitude=lon,
                                                                reply_markup=types.ReplyKeyboardRemove())
                                await message.bot.send_message(message.from_user.id, "Геолокация👆", reply_markup=ibt_connect_to_party)

                            else:
                                cart = await buffer_def.cart(item, my_users)
                                ibt_connect_to_party = await buffer_def.keyboard_party_list(counter, item, parse)

                                await message.bot.send_message(message.from_user.id, cart,
                                                               reply_markup=ibt_connect_to_party)

                        if counter == 4:
                            break

                    if party_exists is False:
                        await message.bot.send_message(message.from_user.id, "<b>По данному запросу ничего не найдено.</b>\n"
                                                                             "<b>Проверьте данные или создайте свою пати</b>",
                                                       reply_markup=ikb_help)

                else:
                    url_with_category_and_city = MAIN_PARTY_LIST_URL + f"{data['category']}/"+f"{data['city']}/" + "?format=json&page="
                    data['url'] = url_with_category_and_city
                    full_url_with_category_and_city = url_with_category_and_city + str(1)

                    parse = json_parse_partys.get_json(url=full_url_with_category_and_city)
                    parse_result = parse.get("results")
                    counter = 0

                    party_exists = False
                    for item in parse_result:
                        if data['city'] == item.get('city'):
                            party_exists = True
                            counter += 1
                        if party_exists:

                            my_users = await buffer_def.users(item)

                            cart = await buffer_def.cart(item, my_users)
                            if item.get('lat') and item.get('lon') != "-":
                                lat = item.get('lat')
                                lon = item.get('lon')
                                ibt_connect_to_party = await buffer_def.keyboard_party_list(counter, item, parse)

                                await message.bot.send_message(message.from_user.id, cart)
                                await message.bot.send_location(message.from_user.id, latitude=lat, longitude=lon,
                                                                reply_markup=types.ReplyKeyboardRemove())
                                await message.bot.send_message(message.from_user.id, "Геолокация👆", reply_markup=ibt_connect_to_party)

                            else:
                                cart = await buffer_def.cart(item, my_users)
                                ibt_connect_to_party = await buffer_def.keyboard_party_list(counter, item, parse)

                                await message.bot.send_message(message.from_user.id, cart,
                                                               reply_markup=ibt_connect_to_party)
                            if counter == 4:
                                break

                    if party_exists is False:
                        await message.bot.send_message(message.from_user.id, "<b>По данному запросу ничего не найдено.</b>\n"
                                                                             "<b>Проверьте данные или создайте свою пати</b>",
                                                       reply_markup=ikb_help)

            @dp.callback_query_handler(lambda query: query.data == "next_page")
            async def party_list_next_page(message: types.Message):
                """Метод пагинации списка Пати"""
                page_text = message["message"]["reply_markup"]["inline_keyboard"][1]
                for item in page_text:
                    if item["callback_data"] == "next_page":
                        page_number = item["text"]
                page_number = page_number.replace("Страница", "").replace(" ", "")
                next_page = int(page_number) + 1
                previous_page = int(page_number) - 1 if int(page_number) > 2 else 1

                url = data['url'] + page_number
                parse = json_parse_partys.get_json(url=url)
                parse_result = parse.get("results")

                counter = 0

                for item in parse_result:
                    counter += 1

                    my_users = await buffer_def.users(item)
                    cart = await buffer_def.cart(item, my_users)
                    if item.get('lat') and item.get('lon') != "-":
                        lat = item.get('lat')
                        lon = item.get('lon')

                        ibt_connect_to_party = await buffer_def.keyboard_party_list_with_next_page(counter, item, parse, next_page, previous_page, page_number)

                        await message.bot.send_message(message.from_user.id, cart)
                        await message.bot.send_location(message.from_user.id, latitude=lat, longitude=lon,
                                                        reply_markup=types.ReplyKeyboardRemove())
                        await message.bot.send_message(message.from_user.id, "Геолокация👆",
                                                       reply_markup=ibt_connect_to_party)

                    else:
                        cart = await buffer_def.cart(item, my_users)
                        ibt_connect_to_party = await buffer_def.keyboard_party_list_with_next_page(counter, item, parse, next_page, previous_page, page_number)

                        await message.bot.send_message(message.from_user.id, cart,
                                                       reply_markup=ibt_connect_to_party)

                    if counter == 4:
                            break

            await FSMFilter_party.next()

            @dp.callback_query_handler(lambda query: query.data == "previous_page")
            async def party_list_previous_page(message: types.Message):
                """Метод пагинации списка Пати"""
                page_text = message["message"]["reply_markup"]["inline_keyboard"][1]
                for item in page_text:
                    if item["callback_data"] == "previous_page":
                        page_number = item["text"]
                page_number = page_number.replace("Страница", "").replace(" ", "")
                next_page = int(page_number) + 1
                previous_page = int(page_number) - 1 if int(page_number) > 2 else 1

                url = data['url'] + page_number
                parse = json_parse_partys.get_json(url=url)
                parse_result = parse.get("results")

                counter = 0

                # блок формирования сообщения
                for item in parse_result:
                    counter += 1

                    my_users = await buffer_def.users(item)
                    cart = await buffer_def.cart(item, my_users)
                    if item.get('lat') and item.get('lon') != "-":
                        lat = item.get('lat')
                        lon = item.get('lon')

                        ibt_connect_to_party = await buffer_def.keyboard_party_list_with_next_page(counter, item, parse, next_page, previous_page, page_number)

                        await message.bot.send_message(message.from_user.id, cart)
                        await message.bot.send_location(message.from_user.id, latitude=lat, longitude=lon,
                                                        reply_markup=types.ReplyKeyboardRemove())
                        await message.bot.send_message(message.from_user.id, "Геолокация👆",
                                                       reply_markup=ibt_connect_to_party)

                    else:
                        cart = await buffer_def.cart(item, my_users)
                        ibt_connect_to_party = await buffer_def.keyboard_party_list_with_next_page(counter, item, parse,
                                                                                                   next_page, previous_page,
                                                                                                   page_number)

                        await message.bot.send_message(message.from_user.id, cart,
                                                       reply_markup=ibt_connect_to_party)

                    if counter == 4:
                        break
    else:
        await message.bot.send_message(message.from_user.id,
                                       '<b>ОШИБКА! Не создан профиль! Для просмотра пати нужно иметь профиль</b>',
                                       reply_markup=ikb_start)



