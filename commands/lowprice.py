from loader import bot
from telebot.types import Message, CallbackQuery
from API.get_info import city_search, hotel_search, photo_search, display_results
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


@bot.callback_query_handler(state=SurveyStates.city_input, func=lambda x: True)
def city_input_details(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id) as request_dict:
        request_dict['destination_id'] = int(call.data)
    bot.send_message(call.from_user.id, 'Введите дату заезда в формате YYYY-MM-DD')
    bot.set_state(call.from_user.id, SurveyStates.check_in)


@bot.message_handler(state=SurveyStates.check_in)
def city_input_details(message: Message):
    # TODO Внедрить календарь для выбора даты
    with bot.retrieve_data(message.from_user.id) as request_dict:
        request_dict['check_in'] = message.text
    bot.send_message(message.from_user.id, 'Введите дату выезда в формате YYYY-MM-DD')
    bot.set_state(message.from_user.id, SurveyStates.check_out)


@bot.message_handler(state=SurveyStates.check_out)
def city_input_details(message: Message):
    # TODO Внедрить календарь для выбора даты
    with bot.retrieve_data(message.from_user.id) as request_dict:
        request_dict['check_out'] = message.text
    bot.send_message(message.from_user.id, 'Сколько выводить предложений?')
    bot.set_state(message.from_user.id, SurveyStates.amount_of_suggestion)


@bot.message_handler(state=SurveyStates.amount_of_suggestion)
def city_input_details(message: Message):
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['amount_of_suggestion'] = message.text
        dict_of_states = {
            'Да': 'yes',
            'Нет': 'no'
        }
        markup = inline_keyboard(states=dict_of_states, row_width=1)
        bot.send_message(message.from_user.id, 'Загрузить фотографии?', reply_markup=markup)
        bot.set_state(message.from_user.id, SurveyStates.get_photos)
    else:
        bot.send_message(message.from_user.id, 'Необходимо ввести целое число')


@bot.callback_query_handler(state=SurveyStates.get_photos, func=lambda x: True)
def city_input_details(call: CallbackQuery):
    if call.data == 'yes':
        bot.send_message(call.from_user.id, 'Какое количество фотографий?')
        bot.set_state(call.from_user.id, SurveyStates.amount_of_photos)
    elif call.data == 'no':
        bot.set_state(call.from_user.id, SurveyStates.results)
        bot.send_message(call.from_user.id, display_results(bot.retrieve_data()))


@bot.message_handler(state=SurveyStates.amount_of_photos)
def city_input_details(message: Message):
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['amount_of_photos'] = int(message.text)
        bot.set_state(message.from_user.id, SurveyStates.results)
        with bot.retrieve_data(message.from_user.id) as data:
            bot.send_message(message.from_user.id, display_results(data))
    else:
        bot.send_message(message.from_user.id, 'Необходимо ввести целое число')



# with bot.retrieve_data(message.from_user.id) as data:
#     bot.send_message(message.from_user.id, 'Ваш запрос в обработке...')
#     results = hotel_search(
#         city_id=data['destination_id'],
#         check_in=data['check_in'],
#         check_out=data['check_out'],
#         amount_of_suggestion=data['amount_of_suggestion'],
#     )
# for item in results:
#     display = [item['name'], item['address']['streetAddress'], item['ratePlan']['price']['current']]
#     bot.send_message(message.from_user.id, '\n'.join(display))


