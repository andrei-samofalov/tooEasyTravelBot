import requests

from settings import logger
from settings import url_hotel_details, headers


def get_hotel_details(hotel_id: int) -> dict:
    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": hotel_id
    }
    req = requests.request("POST", url_hotel_details, json=payload, headers=headers).json()

    logger.debug(f'Hotel ID.{hotel_id}: additional data received')
    return req
