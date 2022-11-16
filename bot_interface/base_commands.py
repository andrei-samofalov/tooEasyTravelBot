from telebot.types import Message
from settings.config import DEFAULT_COMMANDS
from loader import bot
from telebot.types import BotCommand





def base_commands(my_bot):
    my_bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
