from telebot import TeleBot
from telebot.types import CallbackQuery

from bot_interface.keyboards.inline_keyboard import inline_keyboard
from settings.config import DATE_CONFIG
from settings.states import SurveyStates


def date_error(bot: TeleBot, call: CallbackQuery, current_state: str):
    bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id)

    bot.send_message(text=DATE_CONFIG.get(current_state).get('error_text'),
                     chat_id=call.message.chat.id,
                     reply_markup=inline_keyboard(
                         states={'Понятно': 'got_it'},
                         row_width=1)
                     )

    with bot.retrieve_data(call.from_user.id) as request_data:
        request_data['current_state'] = current_state
    bot.set_state(call.from_user.id, SurveyStates.date_error)
