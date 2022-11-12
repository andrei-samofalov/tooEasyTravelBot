from telebot.types import Message
from settings.config import DEFAULT_COMMANDS
from loader import bot
from telebot.types import BotCommand


@bot.message_handler(commands=['start', 'help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, '\n'.join(text))


def base_commands(my_bot):
    my_bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
