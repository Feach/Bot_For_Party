from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Создание кнопок в handlers.create_user.py
button_man = KeyboardButton('Мужской')
button_woman = KeyboardButton('Женский')

button_next1 = KeyboardButton('Завершить')
button_next2 = KeyboardButton('Далее')


# Группы кнопок (resize_keyboard) нужно что бы кнопки были под размер текста
keyboards_create_gender = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_next = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_next12 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)


# add- добавляет все кнопки попрядку
# row- добавляет кнопки в ряд
# insert- поставит кнопку в ряд если есть место

# keyboards_on_main_menu передать в аргумент reply_makrup в функции что бы покдлючить кнопки
keyboards_create_gender.row(button_man, button_woman)

button_next.add(button_next1)
button_next12.add(button_next2)