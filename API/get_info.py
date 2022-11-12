import requests
from typing import Dict
import json
from settings.config import headers, url_city, url_hotel, url_photos


def city_search(city):
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
        sort: str,
        distance: int,
        max_price: int,
        min_price: int
):
    """
        Запрос к API сайта для получения списка отелей
        :param city_id
        :param check_in
        :param check_out
        :param sort
        :param distance
        :param max_price
        :param min_price

        :return словарь с отелями
    """
    query_ = {
        'destinationId': city_id,
        'pageNumber': '1',
        'pageSize': '100',
        'checkIn': check_in,
        'checkOut': check_out,
        'adults1': '1',
        'sortOrder': sort,
        'locale': 'ru_RU',
        'currency': 'RUB'

    }
    pass


# def photo_search(hotel_id, amount):
    # 'size': 'l'
    # pass
