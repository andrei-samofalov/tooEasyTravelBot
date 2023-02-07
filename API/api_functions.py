from datetime import date, datetime

from telebot.types import InputMediaPhoto

from settings import logger


def photos_output(photos: list, caption: str) -> list[InputMediaPhoto]:
    """ Функция для преобразования выгруженных фотографий
        в формат pyTelegramAPI в количестве, указанном пользователем """
    photos_list = []
    for ind, photo in enumerate(photos):
        if ind == 0:
            photos_list.append(
                InputMediaPhoto(photo, caption=caption, parse_mode='html')
            )
        photos_list.append(InputMediaPhoto(photo))

    logger.debug('Photos have been formatted')
    return photos_list


def total_cost(check_in: datetime, check_out: datetime, cost: float) -> int:
    """ Функция для подсчета общей стоимости проживания """
    days = check_out - check_in
    return round(cost * days.days)


def is_valid_date(d: date) -> bool:
    """
    Проверка даты: формат, следование после текущей
    """
    try:
        if d > datetime.today().date():
            return True
    except (ValueError, TypeError):
        return False
