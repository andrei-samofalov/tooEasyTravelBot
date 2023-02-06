import time
from datetime import datetime

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery, Message, BotCommand

from database import add_trash_message_to_db
from settings import DEFAULT_COMMANDS


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
        if request_data.get('msg_to_delete') is None:
            request_data['msg_to_delete'] = [message.message_id]
        else:
            request_data['msg_to_delete'].append(message.message_id)
    bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


def delete_trash_messages(bot: TeleBot, user_id: str | int) -> None:
    """ Функция удаляет все сообщения, полученные в режиме echo """
    try:
        with bot.retrieve_data(user_id) as request_data:
            if request_data:
                for message_id in request_data.get('msg_to_delete', []):
                    bot.delete_message(user_id, message_id)
                else:
                    request_data['msg_to_delete'] = []
    except (KeyError, ApiTelegramException):
        print('Хранилище памяти еще не инициализировано')
