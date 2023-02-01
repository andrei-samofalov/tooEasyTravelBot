import sqlite3

from .sql_functions import add_user_to_db, add_request_to_db
from .sql_scripts import (CREATE_TABLE_SESSIONS_SQL, CREATE_TABLE_USERS_SQL,
                          ADD_USER_REQUEST_TO_DB_SQL, ADD_USER_TO_DB_SQL)

db_connection = sqlite3.Connection(database='./database/travel_bot.db',
                                   check_same_thread=False,
                                   timeout=0.1)
cursor: sqlite3.Cursor = db_connection.cursor()
cursor.execute(CREATE_TABLE_USERS_SQL)
cursor.execute(CREATE_TABLE_SESSIONS_SQL)
