from loader import bot
from telebot.types import Message
from API.get_info import city_search
from settings.states import SurveyStates
from commands.keyboards.inline_keyboard import inline_keyboard


@bot.message_handler(commands=['lowprice'])
def lower_price(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Введите название города')
    bot.set_state(message.from_user.id, SurveyStates.city_input)


@bot.message_handler(state=SurveyStates.city_input)
def city_input(message: Message):
    dict_of_states = city_search(message.text)

    markup = inline_keyboard(states=dict_of_states, row_width=1)
    bot.send_message(message.from_user.id, 'Уточните запрос:', reply_markup=markup)




