# Модуль взаимствования функций для генерации корзин и клавиатур
import re

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data_base import json_parse_users

from config import PARSE_USER_LIST_URL


async def check_auth(message: types.Message):
    data = json_parse_users.get_json(url=PARSE_USER_LIST_URL)
    is_user_exists = False
    for item in data:
        if str(item.get('user_id')) == "@" + str(message.from_user.username):
            is_user_exists = True
    return is_user_exists


async def users(item):
    """Фунция получения списка пользователей в Пати"""
    users = item.get('users')
    my_users = ""
    for user in users:
       my_user = f"<b>-----------</b>\n{'<b>Имя: </b>'} {user.get('name')}\n" \
                 f"{'<b>Пол: </b>'} {user.get('gender')}\n" \
                 f"{'<b>Возраст: </b>'} {user.get('age')}\n" \
                 f"{'<b>Описание: </b>'} {user.get('discription')}\n" \
                 f"{'<b>ID: </b>'} {user.get('user_id')}\n"
       my_users = my_users + my_user
    return my_users


async def cart(item, my_users):
    """Функция получения корзины со списком пати"""

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
    return cart


async def keyboard_party_list(counter, item, parse):
    """Функция создания клавиатуры пагинации с писке пати(первая страница)"""
    page_count = parse.get('count') // 1

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
            ibt_connect_to_party.row(
                InlineKeyboardButton("-----", callback_data="block_data"),
                InlineKeyboardButton(f"1 | {page_count}", callback_data="block_data"),
                InlineKeyboardButton("Страница 2", callback_data="next_page")
                )
        else:
            ibt_connect_to_party.add(
                InlineKeyboardButton("Достигнут лимит подключений", callback_data="limit"))
            ibt_connect_to_party.row(
                InlineKeyboardButton("-----", callback_data="block_data"),
                InlineKeyboardButton(f"1 | {page_count}", callback_data="block_data"),
                InlineKeyboardButton("Страница 2", callback_data="next_page")
            )

    return ibt_connect_to_party


async def keyboard_party_list_with_next_page(counter, item, parse, next_page, previous_page, page_number):
    """Функция создания клавиатуры пагинации с писке пати(последующие страницы)"""

    page_count = parse.get('count') // 1
    ibt_connect_to_party = InlineKeyboardMarkup()
    ibt_connect_to_party.row_width = 2
    if counter < 1:
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
            if parse.get('previous') is None:
                ibt_connect_to_party.row(
                    InlineKeyboardButton("-----", callback_data="block_data"),
                    InlineKeyboardButton(f"{page_number} | {page_count}", callback_data="block_data"),
                    InlineKeyboardButton(f"{'Страница'} {next_page}", callback_data="next_page"),
                )
            elif parse.get('next'):
                ibt_connect_to_party.row(
                    InlineKeyboardButton(f"{'Страница'} {previous_page}", callback_data="previous_page"),
                    InlineKeyboardButton(f"{page_number} | {page_count}", callback_data="block_data"),
                    InlineKeyboardButton(f"{'Страница'} {next_page}", callback_data="next_page")
                )
            elif parse.get('next') is None:
                ibt_connect_to_party.row(
                    InlineKeyboardButton(f"{'Страница'} {previous_page}", callback_data="previous_page"),
                    InlineKeyboardButton(f"{page_number} | {page_count}", callback_data="block_data"),
                    InlineKeyboardButton("-----", callback_data="block_data")
                )
            elif parse.get('previous'):
                ibt_connect_to_party.row(
                    InlineKeyboardButton(f"{'Страница'} {previous_page}", callback_data="previous_page"),
                    InlineKeyboardButton(f"{page_number} | {page_count}", callback_data="block_data"),
                    InlineKeyboardButton(f"{'Страница'} {next_page}", callback_data="next_page")
                )

        else:
            ibt_connect_to_party.add(
                InlineKeyboardButton("Достигнут лимит подключений", callback_data="limit"))
            if parse.get('previous') is None:
                ibt_connect_to_party.row(
                    InlineKeyboardButton("-----", callback_data="block_data"),
                    InlineKeyboardButton(f"{page_number} | {page_count}", callback_data="block_data"),
                    InlineKeyboardButton(f"{'Страница'} {next_page}", callback_data="next_page"),
                )
            elif parse.get('next'):
                ibt_connect_to_party.row(
                    InlineKeyboardButton(f"{'Страница'} {previous_page}", callback_data="previous_page"),
                    InlineKeyboardButton(f"{page_number} | {page_count}", callback_data="block_data"),
                    InlineKeyboardButton(f"{'Страница'} {next_page}", callback_data="next_page")
                )
            elif parse.get('next') is None:
                ibt_connect_to_party.row(
                    InlineKeyboardButton(f"{'Страница'} {previous_page}", callback_data="previous_page"),
                    InlineKeyboardButton(f"{page_number} | {page_count}", callback_data="block_data"),
                    InlineKeyboardButton("-----", callback_data="block_data")
                )
            elif parse.get('previous'):
                ibt_connect_to_party.row(
                    InlineKeyboardButton(f"{'Страница'} {previous_page}", callback_data="previous_page"),
                    InlineKeyboardButton(f"{page_number} | {page_count}", callback_data="block_data"),
                    InlineKeyboardButton(f"{'Страница'} {next_page}", callback_data="next_page")
                )

    return ibt_connect_to_party