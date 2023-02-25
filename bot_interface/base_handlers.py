from telebot.types import Message

from API.display_result import display_results
from API.models import HotelsRequest
from database import add_user_to_db, is_user_in_database, get_last_request
from loader import bot
from settings import DEFAULT_COMMANDS, HELP_MESSAGE, SurveyStates, logger

__all__ = ['bot_start', 'bot_help', 'bot_setting_up']


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    user = message.from_user
    if not is_user_in_database(user.id):
        add_user_to_db(user)
        logger.info(f'User {user.id} was registered in DB')

    text = [
        'Приветствую тебя, путник!',
        'Этот бот поможет тебе найти отель твоей мечты по всему миру (пока кроме России).',
        'Для справки введи команду /help'
    ]
    bot.send_message(message.from_user.id, '\n\n'.join(text))
    bot.set_state(message.from_user.id, SurveyStates.echo)


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, '\n'.join(text) + HELP_MESSAGE)
    bot.set_state(message.from_user.id, SurveyStates.echo)


@bot.message_handler(commands=['setup'])
def bot_setting_up(message: Message):
    bot.send_message(message.from_user.id, 'Команда в разработке')
    bot.set_state(message.from_user.id, SurveyStates.echo)


@bot.message_handler(commands=['state'])
def bot_setting_up(message: Message):
    curr_state = bot.get_state(message.from_user.id)
    bot.send_message(message.from_user.id, f'{curr_state}')
    bot.set_state(message.from_user.id, SurveyStates.echo)


@bot.message_handler(commands=['repeat'])
def keyboard_listen(message: Message):
    if last_request := get_last_request(message.from_user.id):
        request = HotelsRequest(*last_request)
        display_results(user_id=message.from_user.id, request=request.as_dict())
    else:
        bot.send_message(message.from_user.id, 'Вы еще ничего не искали.')
