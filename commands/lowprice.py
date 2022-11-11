from loader import bot
from telebot.types import Message

@bot.message_handler(commands=['lowerprice'])
def lower_price(message: Message) -> None
    bot.send_message(message.from_user.id, 'Введите название города')
