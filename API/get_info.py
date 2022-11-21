import requests
import time
from datetime import datetime
import json
from typing import Dict
from loader import bot
from settings.config import headers, url_city, url_hotel, url_photos, sort_order
from bot_interface.custom_functions import photos_output, total_cost
from database.data_load import load_to_json, load_to_dict, new_user


def city_search(city: str) -> Dict:
    """
    Запрос к API сайта для получения списка возможных совпадений по запросу города
    """
    query = {'query': city, 'locale': 'ru_RU', 'currency': 'RUB'}
    response = requests.request(
        method='GET', url=url_city, headers=headers, params=query
    )
    if response.status_code == 200:
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
        :param sort
            BEST_SELLER |
            STAR_RATING_HIGHEST_FIRST |
            STAR_RATING_LOWEST_FIRST |
            DISTANCE_FROM_LANDMARK |
            GUEST_RATING |
            PRICE_HIGHEST_FIRST |
            PRICE
        :param max_price
        :param min_price
        :param amount_of_suggestion
        :param command

        :return словарь с отелями
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
    if response.status_code == 200:
        hotels = json.loads(response.text)
        hotels = hotels['data']['body']['searchResults']['results']

        return hotels

    else:
        print(f'Ошибка {response.status_code}')


def photo_search(hotel_id) -> Dict:
    """
    Запрос к API сайта для получения ссылок на фотографии

    :param hotel_id: ID отеля из запроса hotel_search
    :return: список ссылок на фотографии
    """

    querystring = {"id": str(hotel_id)}
    response = requests.request(
        method="GET", url=url_photos, headers=headers, params=querystring
    )
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(f'Ошибка {response.status_code}')


def is_valid_date(date) -> bool:
    try:
        if date > datetime.today().date():
            return True
    except ValueError:
        return False


def display_results(user_id: int) -> None:
    """

    Функция обращается к каждому отелю функцией photo_search, для каждого отеля формирует данные, выводимые в чат бота

    :param user_id: ID пользователя, полученного из message.from_user.id или call.from_user.id
    :return: None
    Результат отправляется в загруженного из loader бота в импортах

    """
    with bot.retrieve_data(user_id) as request_dict:
        bot.send_message(user_id, 'Ваш запрос обрабатывается...')

        results = hotel_search(
            city_id=request_dict.get('destination_id'),
            check_in=request_dict.get('check_in'),
            check_out=request_dict.get('check_out'),
            amount_of_suggestion=request_dict.get('amount_of_suggestion'),
            command=request_dict.get('command'),
            max_price=request_dict.get('max_price'),
            min_price=request_dict.get('min_price'),

        )
        user_dict = new_user(user_id=user_id)
        if results:
            for item in results:
                if request_dict.get('amount_of_photos'):
                    hotel_photos = photo_search(item['id'])
                    if hotel_photos:
                        hotel_photos = photos_output(hotel_photos, amount=request_dict.get('amount_of_photos', 0))
                        bot.send_media_group(user_id, hotel_photos)

                cost_of_journey = total_cost(
                    check_in=request_dict.get('check_in'),
                    check_out=request_dict.get('check_out'),
                    cost=item.get('ratePlan', {}).get('price', {}).get('exactCurrent', 0)
                )
                display_list = [
                    ('<b>Название</b>', f"<a href='https://www.hotels.com/ho{item['id']}'>{item['name']}</a>"),
                    ('<b>Оценка</b>', f"{item.get('guestReviews', {}).get('rating', '-')}"
                                      f"/{item.get('guestReviews', {}).get('scale', '-')}"),
                    ('<b>Адрес</b>', item.get('address', {}).get('streetAddress', 'Нет данных')),
                    ('<b>Расстояние до центра</b>', item.get('landmarks', [])[0]['distance']),
                    ('<b>Цена за ночь</b>', item.get('ratePlan', {}).get('price', {}).get('current', 'Нет данных')),
                    ('<b>Общая стоимость проживания</b>', f'{cost_of_journey:,d} RUB')
                ]
                display = [f'{key}: {value}' for key, value in display_list]
                new_dict = load_to_dict(user_dict=user_dict, command=request_dict['command'],
                                        time=time.strftime('%d.%m.%y %H:%M'),
                                        data_list=display)

                bot.send_message(user_id, '\n'.join(display), disable_web_page_preview=True)
                time.sleep(1)
            else:
                load_to_json(user_id, new_dict)
                bot.send_message(user_id, f'Все результаты выгружены')
        else:
            bot.send_message(user_id, 'По запросу ничего не найдено')
