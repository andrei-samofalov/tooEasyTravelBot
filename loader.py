import telebot
from telebot.storage.memory_storage import StateMemoryStorage

from settings.config import BOT_TOKEN

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(
    BOT_TOKEN,
    parse_mode='html',
    state_storage=state_storage
)

