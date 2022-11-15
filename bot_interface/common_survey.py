from loader import bot
from telebot.types import Message, CallbackQuery
from bot_interface.keyboards.inline_keyboard import inline_keyboard
from API.get_info import city_search, display_results
from settings.states import SurveyStates, CommandStates
import re


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def city_input(message: Message):
    bot.send_message(message.from_user.id, 'Введите название города')
    bot.set_state(message.from_user.id, SurveyStates.city_input)
    if message.text == '/lowprice':
        bot.set_state(message.from_user.id, CommandStates.low_price)
    elif message.text == '/highprice':
        bot.set_state(message.from_user.id, CommandStates.high_price)
    else:
        bot.set_state(message.from_user.id, CommandStates.best_deal)


@bot.message_handler(state=SurveyStates.city_input)
def city_input(message: Message):
    dict_of_states = city_search(message.text)
    if dict_of_states:
        markup = inline_keyboard(states=dict_of_states, row_width=1)
        bot.send_message(message.from_user.id, 'Уточните запрос', reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'По запросу ничего не найдено, введите корректное название населенного пункта')


@bot.callback_query_handler(state=SurveyStates.city_input, func=lambda x: True)
def city_input_details(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id) as request_dict:
        request_dict['destination_id'] = int(call.data)
    bot.send_message(call.from_user.id, 'Введите дату заезда в формате YYYY-MM-DD')
    bot.set_state(call.from_user.id, SurveyStates.check_in)


@bot.message_handler(state=SurveyStates.check_in)
def check_in_input(message: Message):

    if re.match(pattern=r'\d{4}-\d{2}-\d{2}\b', string=message.text):
        # TODO Внедрить календарь для выбора даты
        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['check_in'] = message.text
        bot.send_message(message.from_user.id, 'Введите дату выезда в формате YYYY-MM-DD')
        bot.set_state(message.from_user.id, SurveyStates.check_out)
    else:
        bot.send_message(message.from_user.id, 'Проверьте формат ввода')


@bot.message_handler(state=SurveyStates.check_out)
def check_out_input(message: Message):

    if re.match(pattern=r'\d{4}-\d{2}-\d{2}\b', string=message.text):
        # TODO Внедрить календарь для выбора даты
        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['check_out'] = message.text
        bot.send_message(message.from_user.id, 'Сколько выводить предложений?')
        bot.set_state(message.from_user.id, SurveyStates.amount_of_suggestion)
    else:
        bot.send_message(message.from_user.id, 'Проверьте формат ввода')


@bot.message_handler(state=SurveyStates.amount_of_suggestion)
def get_amount(message: Message):
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['amount_of_suggestion'] = message.text
        dict_of_states = {
            'Да': 'yes',
            'Нет': 'no'
        }
        markup = inline_keyboard(states=dict_of_states, row_width=2)
        bot.send_message(message.from_user.id, 'Загрузить фотографии?', reply_markup=markup)
        bot.set_state(message.from_user.id, SurveyStates.get_photos)
    else:
        bot.send_message(message.from_user.id, 'Необходимо ввести целое число')


@bot.callback_query_handler(state=SurveyStates.get_photos, func=lambda x: True)
def get_photo(call: CallbackQuery):
    if call.data == 'yes':
        bot.send_message(call.from_user.id, 'Какое количество фотографий?')
        bot.set_state(call.from_user.id, SurveyStates.amount_of_photos)
    elif call.data == 'no':
        with bot.retrieve_data(call.from_user.id) as request_dict:
            request_dict['amount_of_suggestion'] = 0
        bot.set_state(call.from_user.id, SurveyStates.results)
        display_results(user_id=call.from_user.id)      # TODO


@bot.message_handler(state=SurveyStates.amount_of_photos)
def get_photo(message: Message):
    if message.text.isdigit():
        bot.set_state(message.from_user.id, SurveyStates.results)
        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['amount_of_photos'] = int(message.text)

        display_results(user_id=message.from_user.id)    # TODO
    else:
        bot.send_message(message.from_user.id, 'Необходимо ввести целое число')


@bot.message_handler(state=SurveyStates.results)
def city_input_details(message: Message):
    bot.send_message(message.from_user.id, 'Проверьте ввод')



