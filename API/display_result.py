import time

from loader import bot
from settings import logger, ECHO_MESSAGE
from .hotel_search_request import hotel_search_v2
from .models import Hotel


def display_results(user_id: int) -> None:
    """
    Функция получает от API список отелей,
    для каждого отеля формирует данные, выводимые в чат бота

    :param user_id: ID пользователя, полученного из message.from_user.id
    или call.from_user.id
    :return: None
    Результат отправляется в бота, импортируемого из модуля loader
    """

    bot.send_message(chat_id=user_id,
                     text='Ваш запрос обрабатывается...')

    with bot.retrieve_data(user_id) as request_dict:
        results: list[Hotel] = hotel_search_v2(
            city_id=request_dict.get('destination_id'),
            check_in=request_dict.get('Дата заезда'),
            check_out=request_dict.get('Дата выезда'),
            amount_of_suggestion=request_dict.get('Кол-во предложений'),
            command=request_dict.get('Команда'),
            max_price=request_dict.get('Максимальная цена'),
            min_price=request_dict.get('Минимальная цена'),
        )
        logger.debug(f'Response in Hotel-model: {results}')

        if results:
            for hotel in results:

                display_hotel: str = hotel.display_data()
                photos = request_dict.get('Кол-во фотографий')

                if photos:
                    hotel_hotel_and_photos = hotel.display_with_photos(photos)
                    bot.send_media_group(chat_id=user_id, media=hotel_hotel_and_photos)
                    continue

                bot.send_message(
                    chat_id=user_id,
                    text=display_hotel,
                    disable_web_page_preview=True)
                time.sleep(0.5)

            else:
                bot.send_message(
                    chat_id=user_id,
                    text='Все результаты выгружены.\n' + ECHO_MESSAGE
                )
        else:
            bot.send_message(
                chat_id=user_id,
                text='По запросу ничего не найдено.\n' + ECHO_MESSAGE
            )
