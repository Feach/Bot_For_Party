# Модуль FSM для создания пати
import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from import_buffer import dp
from config import PARSE_PARTY_LIST_URL

from handlers import my_party

from data_base import party_db, json_parse_partys
from keyboards.client_keyboards import keyboards_create_gender, button_next, button_next12, button_category, button_location, button_choice
from loguru import logger


class FSMCreate_party(StatesGroup):
    """Класс определения переменных FSM"""
    title = State()
    category = State()
    city = State()
    choice = State()
    location = State()
    lat_lon = State()
    age = State()
    discription = State()
    default_users = State()
    max_users = State()
    leader_id = State()


@dp.callback_query_handler(lambda query: query.data == "ibtn_create_party", state='*')
async def proverka_party(message: types.Message):
    """Функция проверки лидера пати на наличие у него созданных пати
        и дальнейшего создания пати"""
    parse = json_parse_partys.get_json(url=PARSE_PARTY_LIST_URL)
    data_parse = parse.get("results")
    is_user_exists = False
    for item in data_parse:
        if str(item.get('leader_id')) == "@"+str(message.from_user.username):
            is_user_exists = True
    if is_user_exists:
        await message.bot.send_message(message.from_user.id, 'Вами уже создана пати')
        await my_party.my_party(message)
    else:
        await FSMCreate_party.title.set()
        await message.bot.send_message(message.from_user.id, 'Создайте пати\n<b>ВАЖНО!</b>\nПройдите процедуру до конца, до уведомления об успешном создании\n\n<b>Введите Тему:</b>')

    @dp.message_handler(state=FSMCreate_party.title)
    async def load_title(message: types.Message, state: FSMContext):
        """Метод получения заголовка"""
        async with state.proxy() as data:
            data['title'] = message.text
        await FSMCreate_party.next()
        await message.bot.send_message(message.from_user.id, '<b>Выберете категорию из списка ниже\n'
                                                             'Или введите категорию вручную:</b>', reply_markup=button_category)

    @dp.message_handler(state=FSMCreate_party.category)
    async def load_category(message: types.Message, state: FSMContext):
        """Метод получения категории"""
        async with state.proxy() as data:
            data['category'] = message.text
            data['category'] = data['category'].lower().capitalize()
        await FSMCreate_party.next()
        await message.bot.send_message(message.from_user.id, '<b>Введите Город:\n</b>Например: Барнаул', reply_markup=ReplyKeyboardRemove())

    @dp.message_handler(state=FSMCreate_party.city)
    async def load_city(message: types.Message, state: FSMContext):
        """Метод получения города"""
        async with state.proxy() as data:
            with open('storage/utils/cities.json') as file:
                read = file.read()
                parse = json.loads(read)
                list = parse.get('city')
                data['city'] = message.text
                data['city'] = data['city'].lower().capitalize()
                is_exists = False
                for item in list:
                    if item.get('name') == data['city']:
                        is_exists = True
                        break
                if is_exists:

                    await message.bot.send_message(message.from_user.id, '<b>Введите локацию:\nИли поделитесь геолокацией</b>',
                                                   reply_markup=button_choice)
                    await FSMCreate_party.next()
                else:
                    await message.bot.send_message(message.from_user.id, '<b>Введеного города не существует.\nПроверьте верно ли внесены данные и попробуйте снова</b>')

    @dp.message_handler(state=FSMCreate_party.choice)
    async def load_choice(message: types.Message, state: FSMContext):
        """Метод получения выбора"""
        async with state.proxy() as data:
            if message.text == "Ввести вручную":
                data['choice'] = message.text
                await message.bot.send_message(message.from_user.id,
                                               '<b>Введите локацию:</b>', reply_markup=ReplyKeyboardRemove())
                await FSMCreate_party.next()
            elif message.text == "Отправить свою локацию":
                data['choice'] = message.text
                await FSMCreate_party.lat_lon.set()
                await message.bot.send_message(message.from_user.id,
                                               '<b>Поделитесь своей геолокацией</b>',
                                               reply_markup=button_location)

    @dp.message_handler(state=FSMCreate_party.location)
    async def load_location(message: types.Message, state: FSMContext):
        """Метод получения локации"""
        async with state.proxy() as data:

            data['location'] = message.text
            data['lat'] = "-"
            data['lon'] = "-"

        await FSMCreate_party.age.set()

        await message.bot.send_message(message.from_user.id, '<b>Введите средний возраст Пати:</b>', reply_markup=ReplyKeyboardRemove())

    @dp.message_handler(state=FSMCreate_party.lat_lon, content_types=['location'])
    async def lat_lon(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            lat = message.location.latitude
            lon = message.location.longitude
            if lat and lon:
                data['location'] = "Указана геолокация"
                data['lat'] = str(lat)
                data['lon'] = str(lon)
                print(type(data['lat']), type(data['lon']))


        await FSMCreate_party.next()

        await message.bot.send_message(message.from_user.id, '<b>Введите средний возраст Пати:</b>', reply_markup=ReplyKeyboardRemove())


    @dp.message_handler(state=FSMCreate_party.age)
    async def load_age(message: types.Message, state: FSMContext):
        """Метод получения среднего возраста"""
        async with state.proxy() as data:
            data['age'] = message.text
            age_valid = data['age'].isdigit()
        if age_valid:
            await FSMCreate_party.next()
            await message.bot.send_message(message.from_user.id, '<b>Введите описание и/или требования:</b>')
        else:
            await message.bot.send_message(message.from_user.id, 'Некоректно введенные данные\n<b>Введите средний возраст Пати (число)</b>')

    @dp.message_handler(state=FSMCreate_party.discription)
    async def load_discription(message: types.Message, state: FSMContext):
        """Метод получения описания"""
        async with state.proxy() as data:
            data['discription'] = message.text
        await FSMCreate_party.next()
        await message.bot.send_message(message.from_user.id, 'Запрос обрабатывается...\nНажмите <b>"Далее"</b>',
                                       reply_markup=button_next12)

    @dp.message_handler(state=FSMCreate_party.default_users)
    async def load_default_users(message: types.Message, state: FSMContext):
        """Метод присваивания начального числа юзеров"""

        async with state.proxy() as data:
            data['default_users'] = 1
        if message.text == "Далее":
            await FSMCreate_party.next()
            await message.bot.send_message(message.from_user.id, '<b>Введите максимальное кол-во пользователей</b>')
        else:
            await message.bot.send_message(message.from_user.id, '<b>Ошибка!</b>\nДля продолжения нажмите кнопку <b>"Далее"</b>',
                                           reply_markup=button_next12)

    @dp.message_handler(state=FSMCreate_party.max_users)
    async def load_max_users(message: types.Message, state: FSMContext):
        """Метод получения максимального кол-ва юзеров"""
        async with state.proxy() as data:
            data['max_users'] = message.text
            max_users_valid = data['max_users'].isdigit()
        if max_users_valid:
            await FSMCreate_party.next()
            await message.bot.send_message(message.from_user.id, 'Чтобы завершить создание - нажмите <b>"Завершить"</b>',
                                reply_markup=button_next)
        else:
            await message.bot.send_message(message.from_user.id, '<b>Введите максимальное кол-во пользователей (число)</b>')

    @dp.message_handler(state=FSMCreate_party.leader_id)
    async def load_leader_id(message: types.Message, state: FSMContext):
        """Метод получения id лидера пати и отправка данных для создания"""

        async with state.proxy() as data:
            data['leader_id'] = "@"+message.from_user.username
        if message.text == "Завершить":
            await party_db.sql_create_party(state)
            await state.finish()
            logger.info(f"{data['leader_id']} создал пати(info)")
            await message.bot.send_message(message.from_user.id, '<b>Пати успешно создано!</b>')
            await my_party.my_party(message)
        else:
            await message.bot.send_message(message.from_user.id, 'Чтобы завершить создание - нажмите <b>"Завершить"</b>',
                                           reply_markup=button_next)

