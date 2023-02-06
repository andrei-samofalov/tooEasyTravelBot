import requests

from settings import url_hotel_details, headers


def get_hotel_details(city_id: int) -> dict:
    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": city_id
    }

    return requests.request("POST", url_hotel_details, json=payload, headers=headers).json()
