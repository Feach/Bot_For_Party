#Файл FSM создания пати

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from import_buffer import dp

from data_base import party_db, json_parse_partys
from keyboards.client_keyboards import keyboards_create_gender, button_next, button_next12

from handlers import my_party


class FSMCreate_party(StatesGroup):
    title = State()
    city = State()
    location = State()
    age = State()
    discription = State()
    default_users = State()
    max_users = State()
    leader_id = State()


# начало создания пати
@dp.callback_query_handler(lambda query: query.data == "ibtn_create_party")
async def proverka_party(message: types.Message): #Проверка наличия пати(имеется ли в БД leader_id)
    await message.bot.send_message(message.from_user.id, 'Подождите запрос обрабатывается')
    parse = json_parse_partys.get_json(url="http://127.0.0.1:8000/party_list/?format=json&page_size=1000")
    data_parse = parse.get("results")
    is_user_exists = False
    for item in data_parse:
        if str(item.get('leader_id')) == str(message.from_user.id):
            is_user_exists = True
    if is_user_exists:
        await message.bot.send_message(message.from_user.id, 'Вами уже создана пати')
        await my_party.my_party(message)
    else:
        await FSMCreate_party.title.set()
        await message.bot.send_message(message.from_user.id, 'Создайте пати\nВАЖНО!\nПройдите процедуру до конца, до уведомления об успешном создании\n\nВведите Тему:')

    # принимаем ответ на запрос темы
    @dp.message_handler(state=FSMCreate_party.title)
    async def load_title(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['title'] = message.text
        await FSMCreate_party.next()
        await message.bot.send_message(message.from_user.id, 'Введите Город:')

    # принимаем ответ на запрос локации
    @dp.message_handler(state=FSMCreate_party.city)
    async def load_city(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['city'] = message.text
            print('11111')
        await FSMCreate_party.next()
        await message.bot.send_message(message.from_user.id, 'Введите локацию:')

    # принимаем ответ на запрос локации
    @dp.message_handler(state=FSMCreate_party.location)
    async def load_location(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['location'] = message.text
        await FSMCreate_party.next()
        await message.bot.send_message(message.from_user.id, 'Введите средний возраст Пати:')

    # принимаем ответ на запрос возраста
    @dp.message_handler(state=FSMCreate_party.age)
    async def load_age(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['age'] = message.text
            age_valid = data['age'].isdigit()
        if age_valid:
            await FSMCreate_party.next()
            await message.bot.send_message(message.from_user.id, 'Введите описание и/или требования:')
        else:
            await message.bot.send_message(message.from_user.id, 'Некоректно введенные данные\nВведите средний возраст Пати (число)')


    # принимаем ответ на запрос описани
    @dp.message_handler(state=FSMCreate_party.discription)
    async def load_discription(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['discription'] = message.text
        await FSMCreate_party.next()
        await message.bot.send_message(message.from_user.id, 'Запрос обрабатывается...\nНажмите "Далее"',
                                       reply_markup=button_next12)

    # принимаем ответ на установку дефолтного значения юзеров (устанавливается при нажатии кнопки выше)
    @dp.message_handler(state=FSMCreate_party.default_users)
    async def load_default_users(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['default_users'] = 1
        if message.text == "Далее":
            await FSMCreate_party.next()
            await message.bot.send_message(message.from_user.id, 'Введите максимальное кол-во пользователей')
        else:
            await message.bot.send_message(message.from_user.id, 'Ошибка!\nДля продолжения нажмите кнопку "Далее"',
                                           reply_markup=button_next12)

    # принимаем ответ на запрос макс. кол-ва юзеров
    @dp.message_handler(state=FSMCreate_party.max_users)
    async def load_max_users(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['max_users'] = message.text
            max_users_valid = data['max_users'].isdigit()
        if max_users_valid:
            await FSMCreate_party.next()
            await message.bot.send_message(message.from_user.id, 'Чтобы завершить создание - нажмите "Завершить"',
                                reply_markup=button_next)
        else:
            await message.bot.send_message(message.from_user.id, 'Введите максимальное кол-во пользователей (число)')

    # принимаем ответ на запрос ID (принимается автоматически по кнопки выше)и отправляем данные в бд
    @dp.message_handler(state=FSMCreate_party.leader_id)
    async def load_leader_id(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['leader_id'] = "@"+message.from_user.username
        if message.text == "Завершить":
            await party_db.sql_create_party(state)
            await state.finish()
            await message.bot.send_message(message.from_user.id, 'Пати успешно создано')
            await my_party.my_party(message)
        else:
            await message.bot.send_message(message.from_user.id, 'Чтобы завершить создание - нажмите "Завершить"',
                                           reply_markup=button_next)

