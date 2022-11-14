import requests
from typing import Dict
import json
from loader import bot
import time
from telebot.types import Message, InputMediaPhoto

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
    max_price: int = 1000000,
    min_price: int = 0,
) -> Dict:

    """
        Запрос к API сайта для получения списка отелей
        :param city_id
        :param check_in
        :param check_out
        :param sort
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
    response = requests.request("GET", url=url_hotel, headers=headers, params=querystring)
    if response.status_code == 200:
        hotels = json.loads(response.text)
        hotels = hotels['data']['body']['searchResults']['results']

        return hotels

    else:
        print(f'Ошибка {response.status_code}')


def photo_search(hotel_id, amount=0):
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
        photos_list = []
        for photo in photos['hotelImages']:
            photos_list.append(InputMediaPhoto(photo['baseUrl'].replace('{size}', 'w')))
        return photos_list[:amount]
    else:
        print(f'Ошибка {response.status_code}')


def display_results(user_id: int, amount_of_photos):
    with bot.retrieve_data(user_id) as request_dict:
        bot.send_message(user_id, 'Ваш запрос в обработке...')

        results = hotel_search(
            city_id=request_dict['destination_id'],
            check_in=request_dict['check_in'],
            check_out=request_dict['check_out'],
            amount_of_suggestion=request_dict['amount_of_suggestion'],
        )
    for item in results:
        hotel_photos = photo_search(item['id'], amount_of_photos)

        display = ['Название отеля:', item['name'], 'Адрес:', item['address']['streetAddress'], item['ratePlan']['price']['current']]
        if hotel_photos:
            bot.send_media_group(user_id, hotel_photos)
        bot.send_message(user_id, '\n'.join(display))
        time.sleep(2)
