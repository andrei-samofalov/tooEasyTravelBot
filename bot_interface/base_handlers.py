from telebot.types import Message

from .bot_functions import delete_trash_messages
from database import add_user_to_db, is_user_in_database
from loader import bot
from settings import DEFAULT_COMMANDS, HELP_MESSAGE, SurveyStates, logger, deprecated


@bot.message_handler(commands=['start'])
def bot_help(message: Message):
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
    delete_trash_messages(bot, message.from_user.id)
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, '\n'.join(text) + HELP_MESSAGE)
    bot.set_state(message.from_user.id, SurveyStates.echo)


@bot.message_handler(commands=['sorting'])
def setting_up(message: Message):
    bot.send_message(message.from_user.id, 'Команда в разработке')
    bot.set_state(message.from_user.id, SurveyStates.echo)


@deprecated
@bot.message_handler(commands=['remove_garbage'])
def clear_echo(message: Message):
    delete_trash_messages(bot, message.from_user.id)
    bot.delete_message(chat_id=message.from_user.id,
                       message_id=message.message_id)
