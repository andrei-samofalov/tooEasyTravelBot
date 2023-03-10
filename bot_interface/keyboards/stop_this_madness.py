from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def keyboard(states: list[str]):
    """ Функция для создания клавиатуры ответа """
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(text=key) for key in states]
    markup.add(*buttons)

    return markup
