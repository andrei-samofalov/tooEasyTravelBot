from telebot.custom_filters import StateFilter

from bot_interface import base_commands
from loader import bot
from settings import logger

if __name__ == '__main__':
    base_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    logger.debug('Starting...')
    bot.infinity_polling(logger_level='debug')
