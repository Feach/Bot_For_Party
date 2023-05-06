# FSM создания пользователя
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from data_base import users_db, json_parse_users
from keyboards.client_keyboards import ikb_profile, keyboards_create_gender, button_next

from text_base.texts import create_user_last

from import_buffer import dp

from handlers import profile

from config import PARSE_USER_LIST_URL


class FSMCreate_user(StatesGroup):
    nikname = State()
    gender = State()
    age = State()
    discription = State()
    user_id = State()


# начало создания юзера
@dp.callback_query_handler(lambda query: query.data == "ibtn_create_user")
async def proverka_logina(message: types.Message): #Проверка авторизации пользователя(имеется ли в БД user_id)
    await message.bot.send_message(message.from_user.id, 'Подождите запрос обрабатывается')
    data = json_parse_users.get_json(url=PARSE_USER_LIST_URL)
    is_user_exists = False

    for item in data:
        if str(item.get('user_id')) == "@"+str(message.from_user.username):
            is_user_exists = True
    if is_user_exists:
        await message.bot.send_message(message.from_user.id, 'У вас уже есть профиль')
        await profile.profile(message)
    else:
        await FSMCreate_user.nikname.set()
        await message.bot.send_message(message.from_user.id, 'ВАЖНО!\nПройдите процедуру до конца, до уведомления об успешном создании\n\nВведите имя')

        # принимаем ответ на запрос ника
        @dp.message_handler(state=FSMCreate_user.nikname)
        async def load_nikname(message : types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['nikname'] = message.text
            await FSMCreate_user.next()
            await message.bot.send_message(message.from_user.id, 'Выберите пол:',
                                reply_markup=keyboards_create_gender)

        # принимаем ответ на запрос пола
        @dp.message_handler(state=FSMCreate_user.gender)
        async def load_gender(message : types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['gender'] = message.text
            if data['gender'] == "Мужской":
                await FSMCreate_user.next()
                await message.bot.send_message(message.from_user.id, 'Введите ваш возраст:')
            elif data['gender'] == "Женский":
                await FSMCreate_user.next()
                await message.bot.send_message(message.from_user.id, 'Введите ваш возраст:')
            else:
                await message.bot.send_message(message.from_user.id, 'Выберите пол (Мужской/Женский)',
                                               reply_markup=keyboards_create_gender)

        # принимаем ответ на запрос возраста
        @dp.message_handler(state=FSMCreate_user.age)
        async def load_age(message : types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['age'] = message.text
                age_valid = data['age'].isdigit()
            if age_valid:
                await FSMCreate_user.next()
                await message.bot.send_message(message.from_user.id, 'Введите описание:')
            else:
                await message.bot.send_message(message.from_user.id, 'Введите ваш возраст (число)')

        # принимаем ответ на запрос описани
        @dp.message_handler(state=FSMCreate_user.discription)
        async def load_discription(message : types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['discription'] = message.text
            await FSMCreate_user.next()
            await message.bot.send_message(message.from_user.id, 'Чтобы завершить создание - нажмите "Завершить"',
                                reply_markup=button_next)

        # принимаем ответ на запрос ID (принимается по нажатию кнопки выше) и отправляем данные в бд
        @dp.message_handler(state=FSMCreate_user.user_id)
        async def load_user_id(message : types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['user_id'] = "@"+message.from_user.username
                data['inside_id'] = message.from_user.id
            if message.text == "Завершить":
                await users_db.sql_create_user(state)
                await profile.profile(message)
                await state.finish()
            else:
                await message.bot.send_message(message.from_user.id, 'Чтобы завершить создание - нажмите кнопку "Завершить"',
                                               reply_markup=button_next)

