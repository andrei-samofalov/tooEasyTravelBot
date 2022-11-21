from typing import Dict, List
from telebot.types import InputMediaPhoto
from datetime import datetime


def photos_output(photos: Dict, amount=0) -> List:
    photos_list = [InputMediaPhoto(photo['baseUrl'].replace('{size}', 'z')) for photo in photos['hotelImages']]
    return photos_list[:amount]


def format_date(date):
    return datetime.strftime(date, "%d/%m/%Y")


def total_cost(check_in: datetime.date, check_out: datetime.date, cost: float) -> int:
    days = check_out - check_in
    return round(cost * days.days)
