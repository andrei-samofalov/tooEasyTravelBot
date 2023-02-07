import multiprocessing
import threading
from threading import Thread
from typing import Any

from jsonpointer import resolve_pointer

from settings import logger
from .get_images_request import get_hotel_details
from .api_functions import photos_output
from .get_details_request import get_hotel_details


class Hotel(Thread):
    _points = {
        'id': '/id',
        'name': '/name',
        'stars': '/star',
        'distance': '/destinationInfo/distanceFromDestination/value',
        'user_rating': '/reviews/score',
        'user_rates': '/reviews/total',
        'price_regular': '/price/strikeOut/amount',
        'price_discount': '/price/lead/amount',
    }
    _add_points = {
        'user_ratings_text': '/data/propertyInfo/reviewInfo/summary/overallScoreWithDescriptionA11y/value',
        'address': '/data/propertyInfo/summary/location/address/addressLine',
        'latitude': '/data/propertyInfo/summary/location/coordinates/latitude',
        'longitude': '/data/propertyInfo/summary/location/coordinates/longitude',
        'add_description': '/data/propertyInfo/summary/location/whatsAround/editorial/content/0',
        'images': '/data/propertyInfo/propertyGallery/images',
    }
    _struct_data: dict
    _more_data: dict
    _address: str
    _images: list
    _images_url: list

    def __init__(self,
                 hotel_data: dict,
                 sem1: threading.Semaphore,
                 sem2: multiprocessing.Semaphore) -> None:
        super().__init__()
        self._data = hotel_data
        self._sem1 = sem1
        self._sem2 = sem2

    def run(self) -> None:
        with self._sem1:
            self._more_data = self._get_additional_hotel_data()

        with self._sem2:
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
        return photos_output(self._images_url, self.display_data(), amount)

    def _resolve_data(self) -> dict[str, Any]:
        return {
            point: resolve_pointer(self._data, self._points[point])
            for point in self._points.keys()
        }

    def _get_additional_hotel_data(self) -> dict:
        return get_hotel_details(self._struct_data.get('id'))

    def _resolve_images(self):
        self._images: list[dict] = resolve_pointer(self._more_data, self._add_points.get('images'))
        self._images_url: list[str] = [
            resolve_pointer(img, '/image/url')
            for img in self._images
        ]

    def _resolve_address(self):
        self._address = resolve_pointer(self._more_data, self._add_points['address'])


class HotelsRequest:
    def __init__(self):
        pass
