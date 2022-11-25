from datetime import datetime

from telebot.types import InputMediaPhoto


def photos_output(photos: dict, caption: str, amount=0) -> list[InputMediaPhoto]:
    """ Функция для преобразования выгруженных фотографий
        в формат pyTelegramAPI в количестве, указанном пользователем """
    photos_list = [
        InputMediaPhoto(photo['baseUrl'].replace('{size}', 'z'), caption=caption, parse_mode='html')
        for photo in photos['hotelImages']
    ]
    return photos_list[:amount]


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
