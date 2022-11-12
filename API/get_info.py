import requests
from typing import Dict
import json

import telebot

from settings.config import headers, url_city, url_hotel, url_photos


def city_search(city):
    """
    Запрос к API сайта для получения списка возможных совпадений по запросу города
    """
    query = {'query': city, 'locale': 'ru_RU', 'currency': 'RUB'}
    response = requests.request(method='GET', url=url_city, headers=headers, params=query)
    if response.status_code == 200:
        dict_city_response = json.loads(response.text)
        dict_city_response = dict_city_response['suggestions'][0]['entities']

        dict_city_destination = {}
        for item in dict_city_response:
            dict_city_destination[item['name']] = item['destinationId']

        return dict_city_destination
    else:
        return f'Ошибка запроса {response.status_code}'


def hotel_search(
    city_id: int,
    check_in: str,
    check_out: str,
    amount_of_suggestion: int = 5,
    sort: str = 'PRICE',
    distance: int = None,
    max_price: int = 1000000,
    min_price: int = 0,
) -> Dict:
    """
        Запрос к API сайта для получения списка отелей
        :param city_id
        :param check_in
        :param check_out
        :param sort
        :param distance
        :param max_price
        :param min_price
        :param amount_of_suggestion

        :return словарь с отелями
    """

    querystring = {
        "destinationId": city_id,
        "pageNumber": "1",
        "pageSize": amount_of_suggestion,
        "checkIn": check_in,
        "checkOut": check_out,
        "adults1": "1",
        "sortOrder": sort,
        "locale": "ru_RU",
        "currency": "RUB",
        "priceMin": min_price,
        "priceMax": max_price,

    }
    print('Запускается функция hotel_search')
    response = requests.request("GET", url=url_hotel, headers=headers, params=querystring)
    if response.status_code == 200:
        hotels = json.loads(response.text)
        hotels = hotels['data']['body']['searchResults']['results']

        return hotels

    else:
        print(f'Ошибка {response.status_code}')


def photo_search(hotel_id, amount):
    """
    Запрос к API сайта для получения ссылок на фотографии

    :param hotel_id: ID отеля из запроса hotel_search
    :param amount: количество фотографий, которые необходимо выгрузить

    :return: список/множество ссылок на фотографии
    """

    querystring = {"id": str(hotel_id)}
    response = requests.request("GET", url=url_photos, headers=headers, params=querystring)
    if response.status_code == 200:
        photos = json.loads(response.text)
        print(photos)
    # 'size': 'l'
    pass


def display_results(results: Dict):
    display = []
    for key in results.keys():
        display.append(f'{key}: {results[key]}')
    return '\n'.join(display)
