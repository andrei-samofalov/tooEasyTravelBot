import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены, т.к. отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

# город, ID районов города
url_city = "https://hotels4.p.rapidapi.com/locations/v2/search"
# ID города, гостиница, адрес, цена, удаленность от центра
url_hotel = "https://hotels4.p.rapidapi.com/properties/list"
# фото гостиницы по ID
url_photos = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": RAPID_API_KEY
}

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку по командам'),
    ('lowprice', 'Вывести список самых дешевых отелей'),
    ('highprice', 'Вывести список самых дорогих отелей'),
    ('bestdeal', 'Вывести список отелей по заданным параметрам'),
    ('history', 'Показать историю поиска отелей')
)

sort_order = {
    '/lowprice': 'PRICE',
    '/highprice': 'PRICE_HIGHEST_FIRST',
    '/bestdeal': 'DISTANCE_FROM_LANDMARK'
}

MAX_HOTELS = 25
MAX_PHOTOS = 10