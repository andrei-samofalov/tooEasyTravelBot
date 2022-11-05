from settings import TOKEN
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Наберите команду /hello_world')


@dp.message_handler(commands=['hello_world'])
async def hello_world(message):
    await message.answer('Hello World')


@dp.message_handler(content_types=['text'])
async def incoming_messages(message):
    if message.text.lower() == 'привет':
        await message.reply('Привет тебе, путник')
    else:
        await message.answer('Моя твоя не понимать...')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
