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
    destination_id TEXT,
    destination_name TEXT,
    check_in TEXT,
    check_out TEXT,
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

ADD_USER = """
    insert or ignore into users (id, first_name, last_name, 
                                username, language_code) 
    VALUES (?, ?, ?, ?, ?) 
"""

IS_USER_IN_DB = """
SELECT 
    EXISTS(
    SELECT * 
        FROM users
        WHERE id = ?);
"""

ADD_USER_REQUEST = """
    insert into `sessions` (user_id, command, query_time, 
                            destination_id, destination_name, 
                            check_in, check_out, offer_amount, 
                            photo_amount)
    values (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

ADD_TRASH_MESSAGE = """
INSERT INTO `misc` (user_id, message, `timestamp`) 
VALUES (?, ?, ?);
"""

GET_USERS = """
SELECT * FROM users;
"""

GET_USER_REQUEST = """
SELECT 
    query_time,
    destination_name, 
    check_in, check_out, 
    offer_amount, photo_amount
FROM sessions
WHERE user_id = ?
ORDER BY id DESC 
LIMIT ?;
"""

GET_LAST_REQUEST = """
SELECT * FROM sessions
WHERE user_id = ?
ORDER BY id DESC 
LIMIT 1;
"""
