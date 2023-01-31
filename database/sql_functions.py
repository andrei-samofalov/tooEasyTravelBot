import sqlite3

from telebot.types import User

from .sql_scripts import ADD_USER_REQUEST_TO_DB_SQL, ADD_USER_TO_DB_SQL


def add_request_to_db(conn: sqlite3.Connection, c: sqlite3.Cursor, user_id: int,
                      timestamp: str, request_dict: dict) -> None:
    with conn:
        c.execute(
            ADD_USER_REQUEST_TO_DB_SQL,
            (
                user_id,
                request_dict.get('Команда'),
                timestamp,
                request_dict.get('destination_id'),
                request_dict.get('Населенный пункт'),
                request_dict.get('Дата заезда'),
                request_dict.get('Дата выезда'),
                request_dict.get('Минимальная цена'),
                request_dict.get('Максимальная цена'),
                request_dict.get('Расстояние до центра'),
                request_dict.get('Кол-во предложений'),
                request_dict.get('Кол-во фотографий')
            )
        )


def add_user_to_db(conn: sqlite3.Connection, c: sqlite3.Cursor, user: User) -> bool:
    try:
        with conn:
            c.execute(
                ADD_USER_TO_DB_SQL,
                (
                    user.id,
                    user.first_name,
                    user.last_name,
                    user.username,
                    user.language_code
                )
            )
        return True

    except sqlite3.IntegrityError:
        return False
