# Модуль создания кнопок в боте

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

ibtn_create_user = InlineKeyboardButton('Создать профиль', callback_data='ibtn_create_user')
ibtn_create_party = InlineKeyboardButton('Создать Пати', callback_data='ibtn_create_party')
ibtn_party_list = InlineKeyboardButton('Список Пати', callback_data='ibtn_party_list')
ibtn_connect_to_party = InlineKeyboardButton('Подключиться к Пати', callback_data='ibtn_connect_to_party')
ibtn_profile = InlineKeyboardButton('Профиль', callback_data='ibtn_profile')
ibtn_update_profile = InlineKeyboardButton('Редактировать', callback_data='ibtn_update_profile')
ibtn_my_party = InlineKeyboardButton('Моя пати', callback_data='ibtn_my_party')
ibtn_delete_user = InlineKeyboardButton('Удалить профиль', callback_data='ibtn_delete_user')
ibtn_delete_party = InlineKeyboardButton('Удалить пати', callback_data='ibtn_delete_party')
ibtn_leave_party = InlineKeyboardButton('Выйти из пати', callback_data='ibtn_leave_party')
ibtn_delete_user_yes = InlineKeyboardButton('Да', callback_data='ibtn_delete_user_yes')
ibtn_delete_user_no = InlineKeyboardButton('Нет', callback_data='ibtn_delete_user_no')
ibtn_delete_party_yes = InlineKeyboardButton('Да', callback_data='ibtn_delete_party_yes')
ibtn_delete_party_no = InlineKeyboardButton('Нет', callback_data='ibtn_delete_party_no')
# -------
ibtn_previous = InlineKeyboardButton('Назад', callback_data='ibtn_previous')
ibtn_next = InlineKeyboardButton('Далее', callback_data='ibtn_next')
# -----------
button_yes = KeyboardButton('Да')
button_no = KeyboardButton('Нет')
#------------
button_next_page = KeyboardButton('Далее')
button_previous_page = KeyboardButton('Назад')
# -------------
button_man = KeyboardButton('Мужской')
button_woman = KeyboardButton('Женский')
# ----------------
button_next1 = KeyboardButton('Завершить')
button_next2 = KeyboardButton('Далее')
# -----------------
button_club = KeyboardButton('Клуб')
button_bar = KeyboardButton('Бар')
button_cafe = KeyboardButton('Кафе')
button_restoran = KeyboardButton('Ресторан')
button_theater = KeyboardButton('Театр')
button_concert = KeyboardButton('Концетр')
button_kino = KeyboardButton('Кино')
button_planetary = KeyboardButton('Планетарий')
button_knigi = KeyboardButton('Книги')
button_category = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_category.row(button_club, button_bar, button_cafe)
button_category.row(button_restoran, button_theater, button_concert)
button_category.row(button_kino, button_planetary, button_knigi)
button_category.add(button_next2)

# ---------------
keyboards_create_gender = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_next = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_next12 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_pag = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_yes_no = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_choice = ReplyKeyboardMarkup(resize_keyboard=True)
button_choice.add(KeyboardButton('Отправить свою локацию'))
button_choice.add(KeyboardButton('Ввести вручную'))
button_location = ReplyKeyboardMarkup(resize_keyboard=True)
button_location.add(KeyboardButton('Отправить свою локацию 🗺️', request_location=True))

# ------------------
button_pag.add(button_previous_page, button_next_page)
# ----------
keyboards_create_gender.row(button_man, button_woman)
button_next.add(button_next1)
button_next12.add(button_next2)
# --------
button_yes_no.row(button_no, button_yes)

# --------
button_start_view = KeyboardButton('Начать просмотр')
button_start_view_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_start_view_kb.add(button_start_view)
# --------
ikb_start = InlineKeyboardMarkup().add(ibtn_create_user)
# -------------
ikb_help = InlineKeyboardMarkup().add(ibtn_profile)
ikb_help.add(ibtn_my_party)
ikb_help.row(ibtn_create_party, ibtn_party_list)
# ------------
main_menu = InlineKeyboardMarkup().add(ibtn_profile)
main_menu.row(ibtn_create_party, ibtn_party_list)
# --------
ikb_connect_to_party = InlineKeyboardMarkup().add(ibtn_connect_to_party)
# ------------
ikb_connect_to_party_last = InlineKeyboardMarkup().add(ibtn_profile)
ikb_connect_to_party_last.add(ibtn_my_party)
ikb_connect_to_party_last.row(ibtn_create_party, ibtn_party_list)
# ----
ikb_party_list_last = InlineKeyboardMarkup().add(ibtn_connect_to_party)
ikb_party_list_last.add(ibtn_profile)
ikb_party_list_last.row(ibtn_create_party, ibtn_party_list)
# ----------
ikb_profile = InlineKeyboardMarkup().add(ibtn_my_party)
ikb_profile.row(ibtn_create_party, ibtn_party_list)
ikb_profile.add(ibtn_update_profile)
ikb_profile.add(ibtn_delete_user)
# -----------
ikb_my_party1 = InlineKeyboardMarkup().add(ibtn_profile)
ikb_my_party1.add(ibtn_party_list)
ikb_my_party1.add(ibtn_delete_party)
# -----------------
ikb_my_party2 = InlineKeyboardMarkup().add(ibtn_profile)
ikb_my_party2.row(ibtn_create_party, ibtn_party_list)
# -------------
ikb_pagination = InlineKeyboardMarkup().add(ibtn_connect_to_party)
ikb_pagination.row(ibtn_previous, ibtn_next)
ikb_pagination.row(ibtn_create_party, ibtn_party_list)
# ---------------
ikb_delete_user = InlineKeyboardMarkup().add(ibtn_delete_user)
# -------------
ikb_delete_party = InlineKeyboardMarkup().add(ibtn_delete_party)
# -------
ikb_delete_user_yes_no = InlineKeyboardMarkup().row(ibtn_delete_user_no, ibtn_delete_user_yes)
ikb_delete_party_yes_no = InlineKeyboardMarkup().row(ibtn_delete_party_no, ibtn_delete_party_yes)


