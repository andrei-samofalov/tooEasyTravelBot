from settings.config import DEFAULT_COMMANDS
from telebot.types import BotCommand
from datetime import datetime


def base_commands(my_bot):
    my_bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )


