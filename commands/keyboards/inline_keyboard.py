from typing import Dict
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_keyboard(states: Dict[str, str], row_width: int = 2) -> InlineKeyboardMarkup:
    """
    Функция для создания клавиатур типа Inline
    :param: states - словарь со значениями:
                key: str - текст кнопки
                value: str - значение callback_data
    :param: row_width: int - занимаемое кнопкой пространство
                            фактически означает количество кнопок в линии
                            (по умолчанию - две кнопки на линию)
    """
    markup_keyboard = InlineKeyboardMarkup()
    for key, value in states.items():
        markup_keyboard.add(InlineKeyboardButton(text=key, callback_data=value), row_width=row_width)

    return markup_keyboard
