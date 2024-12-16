from datetime import date, datetime

from telebot.types import InputMediaPhoto

from settings import logger

__all__ = ["photos_output", "is_valid_date"]


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


def is_valid_date(d: date) -> bool:
    """
    Проверка даты: формат, следование после текущей
    """
    try:
        if d > datetime.today().date():
            return True
    except (ValueError, TypeError):
        return False
