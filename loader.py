import telebot
from settings.config import BOT_TOKEN
from telebot.storage.memory_storage import StateMemoryStorage


state_storage = StateMemoryStorage()

bot = telebot.TeleBot(
    BOT_TOKEN,
    parse_mode='html',
    state_storage=state_storage
)

