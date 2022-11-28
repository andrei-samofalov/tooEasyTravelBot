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
    ('start', 'запустить бота'),
    ('help', 'вывести справку'),
    ('lowprice', 'искать самые дешевые отели'),
    ('highprice', 'искать самые дорогие отели'),
    ('bestdeal', 'искать отели по заданным параметрам'),
    ('history', 'показать историю поиска отелей'),
    ('remove_garbage', 'очистить чат от мусора')
)

sort_order = {
    '/lowprice': 'PRICE',
    '/highprice': 'PRICE_HIGHEST_FIRST',
    '/bestdeal': 'DISTANCE_FROM_LANDMARK'
}

MIN_NUM = 1
MAX_HOTELS = 25
MAX_PHOTOS = 10

NUM_ERROR = 'Необходимо ввести любое положительное число'
INT_ERROR = 'Введите целое положительное число'

HELP_MESSAGE = '\n\n' \
               '✔ Все числа, которые потребуется ввести, должны быть целыми и положительными;\n' \
               '✔ Дата заезда должна быть не раньше даты, следующей за сегодняшним днем;\n' \
               '✔ Дата выезда должна быть не раньше даты, следующей за датой заезда;\n' \
               f'✔ Максимальное доступное к выгрузке количество отелей - {MAX_HOTELS};\n' \
               f'✔ Максимальное доступное к выгрузке количество фотографий отелей - {MAX_PHOTOS}.\n'

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
