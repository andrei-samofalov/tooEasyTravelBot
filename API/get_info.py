import time
from datetime import datetime, date
from http import HTTPStatus

import requests

from loader import bot
from settings import (headers, logger, sort_order, url_city_v3, url_hotel_v2, ECHO_MESSAGE)
from .models import Hotel


def city_search_v3(city: str) -> dict:
    """
    Запрос к API сайта для получения списка возможных совпадений по запросу города
    :param city: str, ID местоположения.
    :return dict
    """
    querystring = {"q": city, "locale": "ru_RU"}
    response = requests.request("GET", url_city_v3, headers=headers, params=querystring)
    if response.status_code == HTTPStatus.OK:
        cities_list = response.json().get('sr', [])

        dict_city_destination = {}
        for item in cities_list:
            if item['type'] == 'CITY':
                dict_city_destination[
                    item.get('regionNames', {}).get('displayName', 'Error')
                ] = item.get('gaiaId', 0)

        return dict_city_destination
    else:
        logger.error(f'Error {response.status_code}')


def hotel_search_v2(city_id: str, check_in: date, check_out: date,
                    amount_of_suggestion: int, command: str,
                    max_price: int = 1000000, min_price: int = 1) -> list[Hotel]:
    """
    Запрос к API сайта для получения списка отелей
    """

    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": city_id},
        "checkInDate": {
            "day": check_in.day,
            "month": check_in.month,
            "year": check_in.year
        },
        "checkOutDate": {
            "day": check_out.day,
            "month": check_out.month,
            "year": check_out.year
        },
        "rooms": [
            {
                "adults": 1,
                "children": []
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": amount_of_suggestion,
        "sort": sort_order[command],
        "filters": {"price": {
            "max": max_price,
            "min": min_price
        }}
    }
    response = requests.request("POST", url_hotel_v2, json=payload, headers=headers)
    logger.debug(f'{response=}')
    if response.status_code == HTTPStatus.OK:
        try:
            hotels = response.json()['data']['propertySearch']['properties']
            return [Hotel(*hotel) for hotel in hotels]
        except KeyError:
            return []
    else:
        logger.error(f'Error {response.status_code}')


def is_valid_date(d: date) -> bool:
    """
    Проверка даты: формат, следование после текущей
    """
    try:
        if d > datetime.today().date():
            return True
    except (ValueError, TypeError):
        return False


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
                display_hotel: list = hotel.display_data()
                photos = request_dict.get('Кол-во фотографий')
                if photos:
                    hotel_photos: list = hotel.get_images()

                bot.send_message(
                    chat_id=user_id,
                    text='\n'.join(display_hotel),
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
