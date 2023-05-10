# Модуль FSM для обновления данных юзера
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from import_buffer import dp

from handlers import profile

from data_base import users_db, json_parse_users
from keyboards.client_keyboards import ikb_profile, keyboards_create_gender, button_next


class FSMUpdate_user(StatesGroup):
    """Класс определения переменных FSM"""
    nikname = State()
    gender = State()
    age = State()
    discription = State()
    user_id = State()


@dp.callback_query_handler(lambda query: query.data == "ibtn_update_profile", state='*')
async def proverka_logina(message: types.Message):
    """Функция запуска FSM для изменения данных о пользователе """
    await FSMUpdate_user.nikname.set()
    await message.bot.send_message(message.from_user.id, '<b>ВАЖНО!</b>\nПройдите процедуру до конца, до уведомления об успешном изменении\n\n<b>Введите имя</b>')

    @dp.message_handler(state=FSMUpdate_user.nikname)
    async def load_nikname(message : types.Message, state: FSMContext):
        """Метод получения имени"""
        async with state.proxy() as data:
            data['nikname'] = message.text
        await FSMUpdate_user.next()
        await message.bot.send_message(message.from_user.id, '<b>Выберите пол:</b>',
                            reply_markup=keyboards_create_gender)

    @dp.message_handler(state=FSMUpdate_user.gender)
    async def load_gender(message: types.Message, state: FSMContext):
        """Метод получения пола"""
        async with state.proxy() as data:
            data['gender'] = message.text
        if data['gender'] == "Мужской":
            await FSMUpdate_user.next()
            await message.bot.send_message(message.from_user.id, '<b>Введите ваш возраст:</b>')
        elif data['gender'] == "Женский":
            await FSMUpdate_user.next()
            await message.bot.send_message(message.from_user.id, '<b>Введите ваш возраст:</b>')
        else:
            await message.bot.send_message(message.from_user.id, 'Выберите пол (<b>Мужской/Женский</b>)',
                                           reply_markup=keyboards_create_gender)

    @dp.message_handler(state=FSMUpdate_user.age)
    async def load_age(message: types.Message, state: FSMContext):
        """Метод получения возраста"""
        async with state.proxy() as data:
            data['age'] = message.text
            age_valid = data['age'].isdigit()
        if age_valid:
            await FSMUpdate_user.next()
            await message.bot.send_message(message.from_user.id, '<b>Введите описание:</b>')
        else:
            await message.bot.send_message(message.from_user.id, '<b>Введите ваш возраст (число)</b>')

    @dp.message_handler(state=FSMUpdate_user.discription)
    async def load_discription(message : types.Message, state: FSMContext):
        """Метод получения описания"""
        async with state.proxy() as data:
            data['discription'] = message.text
        await FSMUpdate_user.next()
        await message.bot.send_message(message.from_user.id, 'Чтобы завершить создание - нажмите <b>"Завершить"</b>',
                            reply_markup=button_next)

    @dp.message_handler(state=FSMUpdate_user.user_id)
    async def load_user_id(message: types.Message, state: FSMContext):
        """Метод получения user_id и отправка данных для регистрации"""
        async with state.proxy() as data:
            data['user_id'] = "@" + message.from_user.username
        if message.text == "Завершить":
            await users_db.sql_create_user(state)
            await profile.profile(message)
            await state.finish()
        else:
            await message.bot.send_message(message.from_user.id,
                                           'Чтобы завершить создание - нажмите кнопку <b>"Завершить"</b>',
                                           reply_markup=button_next)

