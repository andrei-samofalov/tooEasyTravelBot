from telebot.types import BotCommand, Message

from bot_interface.custom_functions import delete_trash_messages
from loader import bot
from database import db_connection, cursor, add_user_to_db
from settings import DEFAULT_COMMANDS, HELP_MESSAGE, SurveyStates, logger


def base_commands(my_bot):
    my_bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )


@bot.message_handler(commands=['start'])
def bot_help(message: Message):

    user = message.from_user
    if add_user_to_db(db_connection, cursor, user) is True:
        logger.info(f'User {user.id} was registered in DB')

    text = [
        'Приветствую тебя, путник!',
        'Этот бот поможет тебе найти отель твоей мечты по всему миру (пока кроме России).',
        'Ты можешь попросить бота показать отели с сортировкой по цене: от самых низких и наоборот, '
        'задать диапазон цен и удаленность от центра города.',
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


@bot.message_handler(commands=['remove_garbage'])
def clear_echo(message: Message):
    delete_trash_messages(bot, message.from_user.id)
    bot.delete_message(chat_id=message.from_user.id,
                       message_id=message.message_id)