from telebot.custom_filters import StateFilter

from bot_interface import base_commands
from loader import bot

if __name__ == '__main__':
    base_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()
