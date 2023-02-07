import telebot
from telebot.storage.memory_storage import StateMemoryStorage

from settings import BOT_TOKEN

bot = telebot.TeleBot(
    BOT_TOKEN,
    parse_mode='html',
    state_storage=StateMemoryStorage()
)
