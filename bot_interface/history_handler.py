import time

from telebot.types import Message

from bot_interface import history_display
from database import get_request_from_db
from loader import bot
from settings import ECHO_MESSAGE, INT_ERROR, SurveyStates


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    """ Хэндлер, реагирует на команду /history,
        запрашивает количество отелей, которые нужно отобразить """
    # delete_trash_messages(bot, message.from_user.id)
    bot.send_message(chat_id=message.from_user.id,
                     text='Какое количество последних запросов вывести?')
    bot.set_state(message.from_user.id, SurveyStates.history)


@bot.message_handler(state=SurveyStates.history)
def get_history(message: Message) -> None:
    """ Хэндлер, реагирует на введенное количество отелей для выгрузки.
        Обращается к файлу /data_base.json и выгружает оттуда последние
        N запросов пользователя по ID пользователя Телеграм """

    if message.text.isdigit():
        amount = int(message.text)
        user_requests = get_request_from_db(
            user=message.from_user,
            amount=amount
        )
        for req in user_requests:
            formatted_text = history_display(row=req)
            bot.send_message(
                chat_id=message.from_user.id,
                text=formatted_text
            )
            time.sleep(0.5)
        else:
            bot.send_message(chat_id=message.from_user.id, text=ECHO_MESSAGE)
            bot.set_state(user_id=message.from_user.id, state=SurveyStates.echo)

    else:
        bot.send_message(chat_id=message.from_user.id, text=INT_ERROR)
