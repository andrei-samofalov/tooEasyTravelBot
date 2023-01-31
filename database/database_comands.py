import sqlite3


def create_user_table(c: sqlite3.Cursor) -> None:
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


def create_session(c: sqlite3.Cursor) -> None:
    c.executescript("""
    create table if not exists `sessions` (
    user_id integer,
    command text,
    
    
    )
    """)


add_user_sql = """
    insert or ignore into users (id, first_name, last_name, username, language_code) 
    VALUES (?, ?, ?, ?, ?) 
    """

