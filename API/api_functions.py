from datetime import date, datetime

from telebot.types import InputMediaPhoto

from settings import logger


def photos_output(photos: list, caption: str, amount=0) -> list[InputMediaPhoto]:
    """ Функция для преобразования выгруженных фотографий
        в формат pyTelegramAPI в количестве, указанном пользователем """
    photos_list = [
        InputMediaPhoto(photo, caption=caption, parse_mode='html')
        for photo in photos
    ]

    logger.info(f'{photos_list=}')
    photos_wo_caption = [
        InputMediaPhoto(photo)
        if amount > 1 else [] for photo in photos
    ]
    logger.info(f'{photos_wo_caption=}')
    first_photo = photos_list[:1]
    other_photos = photos_wo_caption[1:amount]
    return first_photo + other_photos


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
