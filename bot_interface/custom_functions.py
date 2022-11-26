from datetime import datetime

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery, InputMediaPhoto, Message


def photos_output(photos: dict, caption: str, amount=0) -> list[InputMediaPhoto]:
    """ Функция для преобразования выгруженных фотографий
        в формат pyTelegramAPI в количестве, указанном пользователем """
    photos_list = [
        InputMediaPhoto(photo['baseUrl'].replace('{size}', 'z'), caption=caption, parse_mode='html')
        for photo in photos['hotelImages']
    ]
    photos_wo_caption = [
        InputMediaPhoto(photo['baseUrl'].replace('{size}', 'z'))
        for photo in photos['hotelImages']
    ]
    first_photo = photos_list[:1]
    other_photos = photos_wo_caption[1:amount]
    return first_photo + other_photos


def format_date(date: datetime) -> datetime.date:
    """ Вспомогательная функция для перевода даты
        в формат %d/%m/%Y """
    return datetime.strftime(date, "%d/%m/%Y")


def total_cost(check_in: datetime, check_out: datetime, cost: float) -> int:
    """ Функция для подсчета общей стоимости проживания """
    days = check_out - check_in
    return round(cost * days.days)


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
        if request_data.get('msg_to_delete') is None:
            request_data['msg_to_delete'] = [message.message_id]
        else:
            request_data['msg_to_delete'].append(message.message_id)
    bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


def delete_echo_messages(bot: TeleBot, user_id: str | int) -> None:
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
