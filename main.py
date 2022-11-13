from loader import bot
from commands.base_commands import base_commands
from telebot.custom_filters import StateFilter

if __name__ == '__main__':
    base_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    bot.polling(non_stop=True, interval=0)

