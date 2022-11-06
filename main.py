from settings import TOKEN
from telebot import TeleBot

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Наберите команду /hello_world')


@bot.message_handler(commands=['hello_world'])
def hello_world(message):
    bot.send_message(message.chat.id, 'Hello World')


@bot.message_handler(content_types=['text'])
def incoming_messages(message):
    if message.text.lower() == 'привет':
        bot.reply_to(message, 'Привет тебе, путник')
    else:
        bot.send_message(message.chat.id, 'Моя твоя не понимать...')


if __name__ == '__main__':
    bot.polling(non_stop=True, timeout=0)
