# Узнать топ самых дешёвых отелей в городе
import requests

req = requests.get('https://rapidapi.com/apidojo/api/hotels4')
print(req.text)