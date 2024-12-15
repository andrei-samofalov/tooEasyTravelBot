import sqlite3
from functools import wraps

from telebot.types import Message, User

import database.sql_scripts as sql
from settings import DATABASE


def db_touch(func: callable):
    @wraps(func)
    def sql_function(*args, **kwargs):
        with sqlite3.Connection(DATABASE) as conn:
            cursor = conn.cursor()
            conn.commit()
            return func(cursor, *args, **kwargs)

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
            request_dict.get('command'),
            timestamp,
            request_dict.get('region_id'),
            request_dict.get('city'),
            request_dict.get('check_in'),
            request_dict.get('check_out'),
            request_dict.get('hotels_amount'),
            request_dict.get('photos_amount')
        )
    )


@db_touch
def get_request_from_db(c: sqlite3.Cursor, user: User, amount: int) -> list:
    c.execute(
        sql.GET_USER_REQUEST,
        (user.id, amount)
    )
    return c.fetchall()


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
        sql.IS_USER_IN_DB,
        (user_id,)
    )
    return c.fetchone()[0]


@db_touch
def get_last_request(c: sqlite3.Cursor, user_id: int) -> tuple:
    c.execute(sql.GET_LAST_REQUEST, (user_id,))
    return c.fetchone()
