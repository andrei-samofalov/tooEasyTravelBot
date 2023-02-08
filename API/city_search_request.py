from http import HTTPStatus

import requests

from settings import headers, logger, url_city_v3

__all__ = ['city_search_v3']


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
