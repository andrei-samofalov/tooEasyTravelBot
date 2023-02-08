import time
from datetime import datetime

from telebot import TeleBot
from telebot.types import BotCommand, CallbackQuery, Message

from database import add_trash_message_to_db
from settings import DEFAULT_COMMANDS

__all__ = ['base_commands', 'format_date',
           'city_name_extract', 'trash_message',
           'history_display']


def base_commands(my_bot):
    my_bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )


def format_date(date: datetime) -> datetime.date:
    """ Вспомогательная функция для перевода даты
        в формат %d/%m/%Y """
    return datetime.strftime(date, "%d/%m/%Y")


def city_name_extract(call_dict: dict, id_search: str) -> str | None:
    """ Функция для извлечения названия населенного пункта,
        выбранного пользователем
        """
    for elem in call_dict['message']['reply_markup']['inline_keyboard']:
        for item in elem:
            if id_search == item['callback_data']:
                return item['text']


def trash_message(bot: TeleBot, message: Message | CallbackQuery) -> None:
    with bot.retrieve_data(message.from_user.id) as request_data:
        curr_time = time.strftime("%d-%m-%Y %H:%M:%S")
        add_trash_message_to_db(message, curr_time)

        request_data.setdefault('msg_to_delete', []).append(message.message_id)
    bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


def history_display(row: tuple) -> str:
    columns = (
        'Date, time',
        'City',
        'Check in',
        'Check out',
        'Hotels',
        'Photos',
    )
    display = dict(zip(columns, row))
    display = [f'<b>{k}</b>: {v}' for k, v in display.items()]
    return "\n".join(display)
