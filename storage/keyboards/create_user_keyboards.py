# Модуль создания кнопок в боте при создание пользователя

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_man = KeyboardButton('Мужской')
button_woman = KeyboardButton('Женский')

button_next1 = KeyboardButton('Завершить')
button_next2 = KeyboardButton('Далее')

keyboards_create_gender = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_next = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_next12 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

keyboards_create_gender.row(button_man, button_woman)

button_next.add(button_next1)
button_next12.add(button_next2)