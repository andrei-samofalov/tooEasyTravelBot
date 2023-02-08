import time

from API.hotel_search_request import hotel_search_v2
from API.models import Hotel
from loader import bot
from settings import ECHO_MESSAGE, logger

__all__ = ['display_results']


def display_results(user_id: int, request: dict) -> None:
    """
    Функция получает от API список отелей,
    для каждого отеля формирует данные, выводимые в чат бота

    :param user_id: ID пользователя
    :param request: словарь с данными запроса
    :return: None
    """

    bot.send_message(chat_id=user_id,
                     text='Ваш запрос обрабатывается...')

    start = time.time()
    logger.debug('Pulling hotels info from API')
    results: [Hotel] = hotel_search_v2(**request)
    photos = request.get('photos_amount')

    if not results:
        bot.send_message(
            chat_id=user_id,
            text='По запросу ничего не найдено.\n' + ECHO_MESSAGE
        )
        return

    for hotel in results:
        hotel.join()

        if photos:
            hotel_hotel_and_photos = hotel.display_with_photos(photos)
            logger.debug(f'{hotel.name}: starting sending messages after {time.time() - start:.3} sec')
            bot.send_media_group(chat_id=user_id, media=hotel_hotel_and_photos)
            continue

        display_hotel: str = hotel.display_data()
        logger.debug(f'{hotel.name}: starting sending messages after {time.time() - start:.3} sec')
        bot.send_message(
            chat_id=user_id,
            text=display_hotel,
            disable_web_page_preview=True)

    else:
        logger.info(f'All results have been displayed after {time.time() - start:.3} sec')
        bot.send_message(
            chat_id=user_id,
            text='Все результаты выгружены.\n' + ECHO_MESSAGE
        )
