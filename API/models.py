import json

from jsonpointer import resolve_pointer

from settings import logger


class Hotel:
    _points = {
        'id': '/id',
        'name': '/name',
        'rating': '/star',
        'availability': '/availability/minRoomsLeft',
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

    def __init__(self, hotel_data: dict) -> None:
        self._data = hotel_data
        self._struct_data = self._resolve_data()

    def _resolve_data(self) -> dict[str, str]:
        return {
            point: resolve_pointer(self._data, self._points[point])
            for point in self._points.keys()
        }

    def display_data(self) -> list[str]:
        return [
            f"<b>{data}</b>: {value}"
            for data, value in self._struct_data.items()
        ]

    def _resolve_images(self, hotel_details: dict) -> list[str]:
        images: list[dict] = resolve_pointer(hotel_details, self._add_points.get('images'))
        img_url = resolve_pointer(images, '/image/url')
        return [img_url for _ in images]

    def get_images(self):
        pass


class HotelsRequest:
    def __init__(self):
        pass


if __name__ == '__main__':
    with open('prop_v2_list.json') as f:
        hotel = json.load(f)
        hot = Hotel(hotel)
        _f = '\n'.join(hot.display_data())
        print(_f)

# https://www.hotels.com/Hotel-Search?
# adults=2&
# d1=2023-02-20&
# d2=2023-02-21&
# destination=Astana%2C%20Kazakhstan&
# endDate=2023-02-21&
# latLong=51.160516%2C71.470365&
# regionId=602528&
# selected=&
# semdtl=&
# sort=DISTANCE&
# startDate=2023-02-20&
# theme=&
# useRewards=false&
# userIntent=
