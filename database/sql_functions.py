import sqlite3
from functools import wraps

from telebot.types import Message, User

import database.sql_scripts as sql
from settings import DATABASE


def create_connection():
    return sqlite3.Connection(DATABASE)


def db_touch(func: callable):
    @wraps(func)
    def sql_function(*args, **kwargs):
        with sqlite3.Connection(DATABASE) as conn:
            cursor = conn.cursor()

            res = func(cursor, *args, **kwargs)
            conn.commit()
            return res

    return sql_function


@db_touch
def create_tables(c: sqlite3.Cursor) -> None:
    c.executescript(sql.CREATE_TABLES)


@db_touch
def add_request_to_db(c: sqlite3.Cursor, user_id: int,
                      timestamp: str, request_dict: dict) -> None:
    c.execute(
        sql.ADD_USER_REQUEST,
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


@db_touch
def add_user_to_db(c: sqlite3.Cursor, user: User) -> None:
    c.execute(
        sql.ADD_USER,
        (
            user.id,
            user.first_name,
            user.last_name,
            user.username,
            user.language_code
        )
    )


@db_touch
def add_trash_message_to_db(
        c: sqlite3.Cursor,
        message: Message,
        timestamp: str
) -> None:
    c.execute(
        sql.ADD_TRASH_MESSAGE,
        (message.from_user.id, message.text, timestamp)
    )


@db_touch
def get_all_messages(c: sqlite3.Cursor) -> list[tuple]:
    c.execute(sql.GET_USERS)
    return c.fetchall()


@db_touch
def is_user_in_database(c: sqlite3.Cursor, user_id: int) -> bool:
    c.execute(
        sql.GET_USER_BY_ID,
        (user_id,)
    )
    return c.fetchone()[0]
