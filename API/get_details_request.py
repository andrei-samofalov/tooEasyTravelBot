import time

import requests

from settings import headers, logger, url_hotel_details


def get_hotel_details(hotel_id: int) -> dict:
    """
    Get hotel details from API
    :param hotel_id: ID of hotel, which information is searching
    :return: json-like Python dictionary
    """
    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": hotel_id
    }
    logger.debug(f'Hotel ID.{hotel_id}: additional data requested')
    start = time.time()
    req = requests.request("POST", url_hotel_details, json=payload, headers=headers).json()

    logger.debug(f'Hotel ID.{hotel_id}: additional data received after {time.time() - start:.3} sec')
    return req
