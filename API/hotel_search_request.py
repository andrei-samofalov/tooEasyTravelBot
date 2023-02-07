import time
from datetime import date
from http import HTTPStatus
from multiprocessing import cpu_count, BoundedSemaphore as pr_Sem
from threading import BoundedSemaphore as th_Sem

import requests

from settings import (headers, logger, sort_order, url_hotel_v2)
from .models import Hotel


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

    if response.status_code == HTTPStatus.OK:
        result = []
        try:
            hotels = response.json()['data']['propertySearch']['properties']

            sem1 = th_Sem(5)        # API limit
            sem2 = pr_Sem(cpu_count())
            for h in hotels:
                result.append(Hotel(h, sem1, sem2))

            for i in result:
                i.start()
                time.sleep(0.05)
            for i in result:
                i.join()

            logger.info(f'All hotels are done with generate data')

        except KeyError as ex:
            logger.error(f"Response doesn't match json structure; {ex.args}")

        return result
    else:
        logger.error(f'Error {response.status_code}: {response.text}')
