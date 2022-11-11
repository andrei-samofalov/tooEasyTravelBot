import requests
import json
from settings.config import headers, url_city, url_hotel, url_photos


def city_search(city):
    query = {'query': city, 'locale': 'ru_RU', 'currency': 'RUB'}
    response = requests.request(method='GET', url=url_city, headers=headers, params=query)
    if response.status_code == 200:
        dict_city_resp = json.loads(response.text)
        dict_city_resp = dict_city_resp['suggestions'][0]['entities']
        return dict_city_resp['name'], dict_city_resp['destinationId']
    else:
        return None


def hotel_search(

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
    {
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


def photo_search(hotel_id, amount):
    # 'size': 'l'
    pass
