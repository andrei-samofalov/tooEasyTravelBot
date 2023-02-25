import os

from dotenv import find_dotenv, load_dotenv

__all__ = [
    'BOT_TOKEN', 'RAPID_API_KEY',
    'url_city_v3', 'url_hotel_v2', 'url_hotel_details', 'headers',
    'DEFAULT_COMMANDS', 'MIN_NUM', 'MAX_HOTELS', 'MAX_PHOTOS',
    'INT_ERROR', 'NUM_ERROR',
    'ECHO_MESSAGE', 'HELP_MESSAGE',
    'DATABASE',
    'DATE_CONFIG', 'sort_order',
]


if not find_dotenv():
    exit('Переменные окружения не загружены, т.к. отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

url_city_v3 = 'https://hotels4.p.rapidapi.com/locations/v3/search'
url_hotel_v2 = "https://hotels4.p.rapidapi.com/properties/v2/list"
url_hotel_details = "https://hotels4.p.rapidapi.com/properties/v2/detail"

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": RAPID_API_KEY
}

DEFAULT_COMMANDS = (
    ('start', 'запустить бота'),
    # ('state', 'вывести состояние'),
    ('search', 'поиск отелей'),  # developing
    ('repeat', 'повторить последний'),
    ('history', 'показать историю поиска'),
    ('help', 'вывести справку'),
)

sort_order = {
    '/search': 'PRICE_LOW_TO_HIGH',
}

MIN_NUM = 1
MAX_HOTELS = 25
MAX_PHOTOS = 10

NUM_ERROR = 'Необходимо ввести любое положительное число'
INT_ERROR = 'Введите целое положительное число'

HELP_MESSAGE = '\n\n' \
               '➡ Все числа, которые потребуется ввести, должны быть целыми и положительными;\n' \
               '➡ Дата заезда должна быть не раньше даты, следующей за сегодняшним днем;\n' \
               '➡ Дата выезда должна быть не раньше даты, следующей за датой заезда;\n' \
               f'❗ Максимальное доступное к выгрузке количество отелей - {MAX_HOTELS};\n' \
               f'❗ Максимальное доступное к выгрузке количество фотографий отелей - {MAX_PHOTOS}.\n'

ECHO_MESSAGE = 'Воспользуйтесь меню бота для продолжения.\n'

DATE_CONFIG = {
    'SurveyStates:check_in': {
        "text": 'Выберите дату заезда',
        "error_text": 'Можно выбрать дату, начиная с завтрашней'
    },
    'SurveyStates:check_out': {
        "text": 'Выберите дату выезда',
        "error_text": 'Дата выезда может быть не ранее '
                      'даты заезда плюс один день'
    }
}

DATABASE = os.getenv('DATABASE')

# ('➡ <b>Название</b>', f"<a href='https://www.hotels.com/ho{item['id']}'>{item['name']}</a>"),
# ('⭐ <b>Звездность</b>', item.get('starRating', 'Нет данных')),
# ('🏆 <b>Оценка посетителей</b>', f"{item.get('guestReviews', {}).get('rating', '- ')}"
#        f"/{item.get('guestReviews', {}).get('scale', ' -')}"),
# ('🗺️ <b>Адрес</b>', item.get('address', {}).get('streetAddress', 'Нет данных')),
# ('📌 <b>Расстояние до центра</b>', item.get('landmarks', [])[0].get('distance', 'Нет данных')),
# ('💵 <b>Цена за ночь</b>', item.get('ratePlan', {}).get('price', {}).get('current', 'Нет данных')),
# ('💰 <b>Общая стоимость проживания</b>', f'{cost_of_journey:,d} RUB')
