import sqlite3


def create_table_users(c: sqlite3.Cursor) -> None:
    c.executescript("""
    begin transaction;
    CREATE TABLE IF NOT EXISTS `users` (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    language_code TEXT);
    commit
    """)


def create_table_sessions(c: sqlite3.Cursor) -> None:
    c.executescript("""
    create table if not exists `sessions` (
    id integer primary key autoincrement,
    user_id integer references users(id),
    command text,
    query_time `timestamp`,
    destination_id integer,
    destination_name text,
    check_in `timestamp`,
    check_out `timestamp`,
    min_price integer,
    max_price integer,
    distance integer,
    offer_amount integer,
    photo_amount integer
    )
    """)


ADD_USER_TO_DB_SQL = """
    insert or ignore into users (id, first_name, last_name, 
                                username, language_code) 
    VALUES (?, ?, ?, ?, ?) 
"""

ADD_USER_REQUEST_TO_DB_SQL = """
    insert into `sessions` (user_id, command, query_time, 
                            destination_id, destination_name, 
                            check_in, check_out, min_price,
                            max_price, distance ,offer_amount, 
                            photo_amount)
    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""