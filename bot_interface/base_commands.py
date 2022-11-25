from telebot.types import BotCommand, Message

from loader import bot
from settings.config import DEFAULT_COMMANDS


def base_commands(my_bot):
    my_bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )


@bot.message_handler(commands=['start'])
def bot_help(message: Message):

    text = [
        'Приветствую тебя, путник!',
        'Этот бот поможет тебе найти отель твоей мечты по всему миру (пока кроме России).',
        'Ты можешь попросить бота показать отели с сортировкой по цене: от самых низких и наоборот, '
        'задать диапазон цен и удаленность от центра города.',
        'Для справки введи команду /help'
    ]
    bot.send_message(message.from_user.id, '\n\n'.join(text))


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, '\n'.join(text))



