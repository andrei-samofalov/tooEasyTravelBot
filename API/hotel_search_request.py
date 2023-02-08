from datetime import date
from http import HTTPStatus
from multiprocessing import Semaphore as pr_Sem
from multiprocessing import cpu_count
from threading import BoundedSemaphore as th_Sem

import requests

from settings import headers, logger, sort_order, url_hotel_v2
from API.models import Hotel

__all__ = ['hotel_search_v2']


def hotel_search_v2(region_id: str, check_in: date, check_out: date,
                    hotels_amount: int, command: str, **kwargs) -> [Hotel]:
    """
    Запрос к API сайта для получения списка отелей
    """

    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": region_id},
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
        "resultsSize": hotels_amount,
        "sort": sort_order[command],
        "filters": {"price": {
            "max": 100000,
            "min": 1
        }}
    }
    response = requests.request("POST", url_hotel_v2, json=payload, headers=headers)

    if response.status_code == HTTPStatus.OK:

        try:
            hotels = response.json()['data']['propertySearch']['properties']

            sem1 = th_Sem(5)  # API limit
            sem2 = pr_Sem(cpu_count())
            for h in hotels:
                hotel = Hotel(h, sem1, sem2)
                yield hotel

            logger.info(f'All hotels are done with generate data')

        except KeyError as ex:
            logger.error(f"Response doesn't match json structure; {ex.args}")

    else:
        logger.error(f'Error {response.status_code}: {response.text}')
