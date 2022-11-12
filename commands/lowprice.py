from loader import bot
from telebot.types import Message, CallbackQuery
from API.get_info import city_search, hotel_search
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


@bot.callback_query_handler(func=lambda x: True)
def city_input_details(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id) as request_dict:
        request_dict['destination_id'] = int(call.data)
    bot.send_message(call.from_user.id, 'Введите дату заезда в формате YYYY-MM-DD')
    bot.set_state(call.from_user.id, SurveyStates.check_in)


@bot.message_handler(state=SurveyStates.check_in)
def city_input_details(message: Message):
    with bot.retrieve_data(message.from_user.id) as request_dict:
        request_dict['check_in'] = message.text
    bot.send_message(message.from_user.id, 'Введите дату выезда в формате YYYY-MM-DD')
    bot.set_state(message.from_user.id, SurveyStates.check_out)


@bot.message_handler(state=SurveyStates.check_out)
def city_input_details(message: Message):
    with bot.retrieve_data(message.from_user.id) as request_dict:
        request_dict['check_out'] = message.text
    bot.send_message(message.from_user.id, 'Сколько выводить предложений?')
    bot.set_state(message.from_user.id, SurveyStates.amount_of_suggestion)


@bot.message_handler(state=SurveyStates.amount_of_suggestion)
def city_input_details(message: Message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['amount_of_suggestion'] = int(message.text)
        print(data)
        hotel_search(
            city_id=data['destination_id'],
            check_in=data['check_in'],
            check_out=data['check_out'],
            amount_of_suggestion=data['amount_of_suggestion'],
        )



