from telebot.types import Message

from bot_interface.custom_functions import trash_message
from loader import bot
from settings.states import SurveyStates


@bot.message_handler(state=[SurveyStates.echo, SurveyStates.check_in,
                            SurveyStates.check_out])
def trash_messages(message: Message) -> None:
    """ Хэндлер, реагирует на любые сообщения пользователя вне опроса.
        Удаляет мусорные сообщения """
    trash_message(bot=bot, message=message)

