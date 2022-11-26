import json
import time
from datetime import datetime
from http import HTTPStatus
from typing import Dict

import requests

from bot_interface.custom_functions import photos_output, total_cost
from database.data_load import (collected_data, load_to_dict, load_to_json,
                                new_user)
from loader import bot
from settings.config import (ECHO_MESSAGE, headers, sort_order, url_city,
                             url_hotel, url_photos)


def city_search(city: str) -> Dict:
    """
    Запрос к API сайта для получения списка возможных совпадений по запросу города
    :param city: str, ID местоположения
    :return dict
    """
    query = {'query': city, 'locale': 'ru_RU', 'currency': 'RUB'}
    response = requests.request(
        method='GET', url=url_city, headers=headers, params=query
    )
    if response.status_code == HTTPStatus.OK:
        dict_city_response = json.loads(response.text)
        dict_city_response = dict_city_response['suggestions'][0]['entities']

        dict_city_destination = {}
        for item in dict_city_response:
            dict_city_destination[item['name']] = item['destinationId']

        return dict_city_destination
    else:
        print(f'Ошибка запроса {response.status_code}')


def hotel_search(city_id: int, check_in: str, check_out: str,
                 amount_of_suggestion: int, command: str,
                 max_price: str = '1000000', min_price: str = '1') -> Dict:

    """
        Запрос к API сайта для получения списка отелей
        :param city_id
        :param check_in
        :param check_out
        :param max_price
        :param min_price
        :param amount_of_suggestion
        :param command

        :return dict: словарь с отелями
    """

    querystring = {
        "destinationId": city_id,
        "pageNumber": "1",
        "pageSize": amount_of_suggestion,
        "checkIn": check_in,
        "checkOut": check_out,
        "adults1": "1",
        "sortOrder": sort_order[command],
        "locale": "ru_RU",
        "currency": "RUB",
        "priceMin": min_price,
        "priceMax": max_price,
    }
    response = requests.request(
        method="GET", url=url_hotel, headers=headers, params=querystring
    )
    if response.status_code == HTTPStatus.OK:
        hotels = json.loads(response.text)
        hotels = hotels['data']['body']['searchResults']['results']

        return hotels

    else:
        print(f'Ошибка {response.status_code}')


def photo_search(hotel_id) -> Dict | int:
    """
    Запрос к API сайта для получения ссылок на фотографии

    :param hotel_id: ID отеля из запроса hotel_search
    :return: список ссылок на фотографии
    """

    querystring = {"id": str(hotel_id)}
    response = requests.request(
        method="GET", url=url_photos, headers=headers, params=querystring
    )
    if response.status_code == HTTPStatus.OK:
        return json.loads(response.text)
    else:
        print(f'Ошибка {response.status_code}')
        return response.status_code


def is_valid_date(date: datetime) -> bool:
    """
    Проверка даты на формат и то, чтобы не была раньше текущей
    :param date: datetime
    :return: bool
    """
    try:
        if date > datetime.today().date():
            return True
    except ValueError:
        return False


def display_results(user_id: int) -> None:
    """

    Функция обращается к каждому отелю функцией photo_search,
    для каждого отеля формирует данные, выводимые в чат бота

    :param user_id: ID пользователя, полученного из message.from_user.id
    или call.from_user.id
    :return: None
    Результат отправляется в загруженного из loader бота в импортах

    """

    bot.send_message(chat_id=user_id,
                     text='Ваш запрос обрабатывается...')

    with bot.retrieve_data(user_id) as request_dict:

        results = hotel_search(
            city_id=request_dict.get('destination_id'),
            check_in=request_dict.get('Дата заезда'),
            check_out=request_dict.get('Дата выезда'),
            amount_of_suggestion=request_dict.get('Кол-во предложений'),
            command=request_dict.get('Команда'),
            max_price=request_dict.get('Максимальная цена'),
            min_price=request_dict.get('Минимальная цена'),
        )

        user_dict = new_user(user_id=user_id)
        if results:
            for item in results:

                cost_of_journey = total_cost(
                    check_in=request_dict.get('Дата заезда'),
                    check_out=request_dict.get('Дата выезда'),
                    cost=item.get('ratePlan', {}).get('price', {}).get('exactCurrent', 0)
                )

                display_list = [
                    ('➡ <b>Название</b>', f"<a href='https://www.hotels.com/ho{item['id']}'>{item['name']}</a>"),
                    ('⭐ <b>Звездность</b>', item.get('starRating', 'Нет данных')),
                    ('🏆 <b>Оценка посетителей</b>', f"{item.get('guestReviews', {}).get('rating', '- ')}"
                                                    f"/{item.get('guestReviews', {}).get('scale', ' -')}"),
                    ('🗺️ <b>Адрес</b>', item.get('address', {}).get('streetAddress', 'Нет данных')),
                    ('📌 <b>Расстояние до центра</b>', item.get('landmarks', [])[0].get('distance', 'Нет данных')),
                    ('💵 <b>Цена за ночь</b>', item.get('ratePlan', {}).get('price', {}).get('current', 'Нет данных')),
                    ('💰 <b>Общая стоимость проживания</b>', f'{cost_of_journey:,d} RUB')
                ]
                display = [f'{key}: {value}' for key, value in display_list]

                new_dict = load_to_dict(user_dict=user_dict, command=collected_data(request_dict),
                                        time=time.strftime('%d.%m.%y %H:%M'), data_list=display)

                if request_dict.get('Кол-во фотографий'):
                    hotel_photos = photo_search(hotel_id=item['id'])

                    # если полученный результат - словарь, то преобразовать в
                    # телеграм-медиа и выгрузить в чат

                    if isinstance(hotel_photos, dict):
                        hotel_photos = photos_output(
                            photos=hotel_photos,
                            amount=request_dict.get('Кол-во фотографий', 0),
                            caption='\n'.join(display)
                        )
                        bot.send_media_group(chat_id=user_id, media=hotel_photos)
                    else:
                        bot.send_message(chat_id=user_id,
                                         text='Не удалось загрузить фотографии')
                else:
                    bot.send_message(chat_id=user_id, text='\n'.join(display),
                                     disable_web_page_preview=True)
                time.sleep(1)
            else:
                load_to_json(user_id=user_id, user_dict=new_dict)
                bot.send_message(
                    chat_id=user_id,
                    text='Все результаты выгружены.\n' + ECHO_MESSAGE
                )
        else:
            bot.send_message(
                chat_id=user_id,
                text='По запросу ничего не найдено.\n' + ECHO_MESSAGE
            )
