import json
from jsonpointer import resolve_pointer


class Hotel:
    _points = {
        'name': '/data/propertyInfo/summary/map/markers/2/title',
        'rating': '/data/propertyInfo/summary/overview/propertyRating/rating',
        'user_rating': '',
        'address': '',
        'center_range': '',
        'price': '',
        'cost': ''
    }
    def __init__(self, hotel_data: dict) -> None:
        # ('➡ <b>Название</b>', f"<a href='https://www.hotels.com/ho{item['id']}'>{item['name']}</a>"),
        # ('⭐ <b>Звездность</b>', item.get('starRating', 'Нет данных')),
        # ('🏆 <b>Оценка посетителей</b>', f"{item.get('guestReviews', {}).get('rating', '- ')}"
        #        f"/{item.get('guestReviews', {}).get('scale', ' -')}"),
        # ('🗺️ <b>Адрес</b>', item.get('address', {}).get('streetAddress', 'Нет данных')),
        # ('📌 <b>Расстояние до центра</b>', item.get('landmarks', [])[0].get('distance', 'Нет данных')),
        # ('💵 <b>Цена за ночь</b>', item.get('ratePlan', {}).get('price', {}).get('current', 'Нет данных')),
        # ('💰 <b>Общая стоимость проживания</b>', f'{cost_of_journey:,d} RUB')
        self._data = hotel_data
        self._name = self._resolve_name()
        self._rating = self._resolve_ratings()

    def _resolve_ratings(self):
        return resolve_pointer(self._data, self._points['rating'])

    def _resolve_name(self):
        return resolve_pointer(self._data, self._points['name'])

    def _resolve_user_ratings(self):
        return resolve_pointer(self._data, self._points['user_rating'])

    def _resolve_address(self):
        return resolve_pointer(self._data, self._points['address'])

    def _resolve_price(self):
        return resolve_pointer(self._data, self._points['price'])

    def _resolve_cost(self):
        return resolve_pointer(self._data, self._points['cost'])

    def display_info(self):
        return {
            'name': self._name,
            'rating': self._rating,
        }


class HotelsRequest:
    def __init__(self):
        pass


with open('prop_v2_details.json') as f:
    hotel = json.load(f)
    hot = Hotel(hotel)
    print(hot.display_info())
