from telebot.custom_filters import StateFilter

from bot_interface.base_commands import base_commands
from loader import bot

if __name__ == '__main__':
    base_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    bot.polling(non_stop=True, interval=0)

# если получится, то добавить кнопку пропустить и выгрузить все варианты по дефолту
# если нет искомого города среди предложений, выдавать об этом сообщение. regexp
