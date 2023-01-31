from . import data_load
from .database_comands import *


db_connection = sqlite3.Connection('./database/travel_bot.db', check_same_thread=False)
cursor = db_connection.cursor()
create_user_table(cursor)
