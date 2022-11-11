import json
from typing import Dict
import requests

url = "https://hotels4.p.rapidapi.com/locations/v2/search"

querystring = {"query":"new york","locale":"en_EN","currency":"RUB"}

headers = {
	"X-RapidAPI-Key": "fa17fa773amsh7b7aa6d40698ffcp12c835jsn0da3ef7ed9c8",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)


# url = "https://hotels4.p.rapidapi.com/locations/search"
#
# querystring = {"query": "new york", "locale":"ru_RU", }
#
# headers = {
# 	"X-RapidAPI-Key": "fa17fa773amsh7b7aa6d40698ffcp12c835jsn0da3ef7ed9c8",
# 	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
# }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
# BEST_SELLER|
# STAR_RATING_HIGHEST_FIRST|
# STAR_RATING_LOWEST_FIRST|
# DISTANCE_FROM_LANDMARK|
# GUEST_RATING|
# PRICE_HIGHEST_FIRST|
# PRICE

w: Dict = json.loads(response.text)
#
# with open('locations.json', 'r') as file:
# 	new_dict: Dict = json.loads(file.read())
# 	# wei = new_dict.get('suggestions')
# 	# print(wei)
# 	for item in new_dict['suggestions'][0]['entities']:
# 		print(item)


#
with open('locations.json', 'w') as file:
	json.dump(w, file, indent=4)
