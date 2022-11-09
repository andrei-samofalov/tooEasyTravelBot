from telebot.types import Message
from settings import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['start', 'help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message, '\n'.join(text))
