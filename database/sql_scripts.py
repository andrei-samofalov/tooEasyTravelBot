CREATE_TABLES = """
    BEGIN TRANSACTION;
    CREATE TABLE IF NOT EXISTS `users` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    language_code TEXT
    );
    CREATE TABLE IF NOT EXISTS `sessions` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    command TEXT,
    query_time TEXT,
    destination_id INTEGER,
    destination_name TEXT,
    check_in TEXT,
    check_out TEXT,
    min_price INTEGER,
    max_price INTEGER,
    distance INTEGER,
    offer_amount INTEGER,
    photo_amount INTEGER
    );
    CREATE TABLE IF NOT EXISTS `misc` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES `users`(id),
    message TEXT,
    `timestamp` TEXT
    );
    COMMIT;
"""


CREATE_TABLE_SESSIONS_SQL = """
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
"""


ADD_USER_TO_DB_SQL = """
    insert into users (id, first_name, last_name, 
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