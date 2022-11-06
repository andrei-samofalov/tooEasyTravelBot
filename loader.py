from settings import TOKEN
from telebot import TeleBot

bot = TeleBot(TOKEN)
bot.polling(non_stop=True, timeout=0)
