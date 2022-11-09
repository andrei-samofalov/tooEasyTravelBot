import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены, т.к. отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

RapidAPIUrl = r"https://hotels4.p.rapidapi.com/"

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('lowprice', 'Вывести список дешевых отелей'),
    ('highprice', 'Вывести список дорогих отелей'),
    ('bestdeal', 'Вывести список отелей по заданным параметрам'),
    ('history', 'Показать историю запросов за {сессию}')
)