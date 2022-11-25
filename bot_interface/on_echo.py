from telebot.types import Message

from loader import bot
from settings.config import ECHO_MESSAGE


@bot.message_handler(content_types=['text'])
def echo(message: Message) -> None:
    """ Хэндлер, реагирует на любые сообщения пользователя вне опроса
        """
    bot.send_message(chat_id=message.from_user.id,
                     text=ECHO_MESSAGE)
