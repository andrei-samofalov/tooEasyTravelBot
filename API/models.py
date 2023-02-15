import multiprocessing
import threading
from dataclasses import dataclass
from datetime import datetime, date
from typing import Any

from jsonpointer import JsonPointerException, resolve_pointer

from API.api_functions import photos_output
from API.get_details_request import get_hotel_details
from settings import logger

__all__ = ['Hotel', 'HotelsRequest']


class Hotel:
    """
    Модель отеля, которая собирает необходимую для отображения в боте информацию.

    Методы `display_data` и `display_with_photos` используются в качестве основных
    """
    # методы по заполнению класса должны быть перенесены за пределы класса #

    _POINTS = {
        'id': '/id',
        'Name': '/name',
        'Address': '/name',
        'Distance from center': '/destinationInfo/distanceFromDestination/value',
        # 'user_rating': '/reviews/score',
        # 'user_rates': '/reviews/total',
        'Price per night': '/price/lead/formatted',
        'Cost': '/price/displayMessages/1/lineItems/0/value'
    }
    _ADD_POINTS = {
        # 'user_ratings_text': '/data/propertyInfo/reviewInfo/summary/overallScoreWithDescriptionA11y/value',
        'address': '/data/propertyInfo/summary/location/address/addressLine',
        # 'latitude': '/data/propertyInfo/summary/location/coordinates/latitude',
        # 'longitude': '/data/propertyInfo/summary/location/coordinates/longitude',
        'add_description': '/data/propertyInfo/summary/location/whatsAround/editorial/content/0',
        'images': '/data/propertyInfo/propertyGallery/images',
    }
    _struct_data: dict
    _more_data: dict
    _address: str
    _msg_with_images: list
    _images_url: list

    def __init__(self, hotel_data: dict) -> None:
        super().__init__()

        self._id = hotel_data['id']
        self.name = f"Hotel ID.{self._id}"
        self._data = hotel_data

    def resolve(self) -> None:
        self._more_data = self._get_additional_hotel_data()
        self._struct_data = self._resolve_data()
        logger.debug(f'{self.name}: data resolved')
        try:
            self._resolve_address()
            logger.debug(f'{self.name}: address resolved')
            self._resolve_images()
        except JsonPointerException as ex:
            logger.error(f'{self.name}: unable to resolve; {ex.args}')

    def display_data(self) -> str:
        return "\n".join(
            f"<b>{data}</b>: {value}"
            for data, value in self._struct_data.items()
        )

    def display_with_photos(self, amount: int):
        return self._msg_with_images[:amount]

    def _resolve_data(self) -> dict[str, Any]:
        return {
            point: resolve_pointer(self._data, self._POINTS[point])
            for point in self._POINTS.keys()
        }

    def _get_additional_hotel_data(self) -> dict:
        return get_hotel_details(self._id)

    def _resolve_images(self):
        self._msg_with_images: list[dict] = resolve_pointer(self._more_data, self._ADD_POINTS.get('images'))

        self._images_url: list[str] = [
            resolve_pointer(img, '/image/url')
            for img in self._msg_with_images
        ]

        self._msg_with_images = photos_output(self._images_url, self.display_data())

    def _resolve_address(self):
        self._struct_data['Address'] = resolve_pointer(self._more_data, self._ADD_POINTS['address'])


@dataclass
class HotelsRequest:
    _id: int
    _userID: int
    _command: str
    _query_time: str
    _regionID: str
    _city: str
    _checkIN: str | date
    _checkOUT: str | date
    _hotelsAmount: int
    _photosAmount: int | None

    def _resolve_date(self):
        self._checkIN = datetime.strptime(self._checkIN, "%Y-%m-%d").date()
        self._checkOUT = datetime.strptime(self._checkOUT, "%Y-%m-%d").date()

    def as_dict(self):
        self._resolve_date()
        return {
            "region_id": self._regionID,
            "check_in": self._checkIN,
            "check_out": self._checkOUT,
            "hotels_amount": self._hotelsAmount,
            "command": self._command,
            "photos_amount": self._photosAmount
        }
