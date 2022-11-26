from telebot.types import Message

from bot_interface.custom_functions import trash_message
from loader import bot
from settings.states import SurveyStates


@bot.message_handler(state=SurveyStates.echo)
def echo(message: Message) -> None:
    """ Хэндлер, реагирует на любые сообщения пользователя вне опроса """
    trash_message(bot, message)

