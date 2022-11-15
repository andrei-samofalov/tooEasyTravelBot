from typing import Dict, List
from telebot.types import InputMediaPhoto


def photos_output(photos: Dict, amount=0) -> List:
    photos_list = [InputMediaPhoto(photo['baseUrl'].replace('{size}', 'z')) for photo in photos['hotelImages']]
    return photos_list[:amount]
