from telebot.types import Message, CallbackQuery
from bot_interface.keyboards.inline_keyboard import inline_keyboard
from API.get_info import *
from settings.states import SurveyStates
from telegram_bot_calendar import DetailedTelegramCalendar
from settings.config import DEFAULT_COMMANDS


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def city_input(message: Message):
    bot.reset_data(message.from_user.id)
    bot.send_message(message.from_user.id, 'Введите название города')
    bot.set_state(message.from_user.id, SurveyStates.city_input)
    with bot.retrieve_data(message.from_user.id) as request_dict:
        request_dict['command'] = message.text


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
        request_dict['destination_id'] = int(call.data)   # TODO если команда такая-то, то state такой, вызов промежуточной функции
        if request_dict['command'] == '/bestdeal':
            bot.set_state(call.from_user.id, SurveyStates.min_price)
            bot.send_message(call.from_user.id, 'Введите минимальную стоимость за сутки (руб)')
        else:
            bot.set_state(call.from_user.id, SurveyStates.check_in)
            calendar_bot, step = DetailedTelegramCalendar().build()
            bot.send_message(call.from_user.id,
                             f"Выберите дату заезда",
                             reply_markup=calendar_bot)


@bot.callback_query_handler(state=SurveyStates.check_in, func=DetailedTelegramCalendar.func())
def calendar(call: CallbackQuery):
    result, key, step = DetailedTelegramCalendar().process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите дату заезда",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif is_valid_date(result):
        bot.edit_message_text(f"{result}",
                              call.message.chat.id,
                              call.message.message_id)
        bot.set_state(call.from_user.id, SurveyStates.check_out)
        with bot.retrieve_data(call.from_user.id) as request_dict:
            request_dict['check_in'] = result
            print(request_dict['check_in'])
        calendar_bot, step = DetailedTelegramCalendar().build()
        bot.send_message(call.from_user.id,
                         f"Выберите дату выезда",
                         reply_markup=calendar_bot)
    else:
        bot.send_message(call.from_user.id, 'Нельзя выбрать прошедшую дату')
        calendar_bot, step = DetailedTelegramCalendar().build()
        bot.send_message(call.from_user.id,
                         f"Выберите дату заезда",
                         reply_markup=calendar_bot)


@bot.callback_query_handler(state=SurveyStates.check_out, func=DetailedTelegramCalendar.func())
def calendar(call: CallbackQuery):
    result, key, step = DetailedTelegramCalendar().process(call.data)
    with bot.retrieve_data(call.from_user.id) as request_dict:

        if not result and key:
            bot.edit_message_text(f"Выберите дату выезда",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif is_valid_date(result) and result - request_dict['check_in'] >= 1:
            bot.edit_message_text(f"{result}",
                                  call.message.chat.id,
                                  call.message.message_id)
            bot.set_state(call.from_user.id, SurveyStates.amount_of_suggestion)
            request_dict['check_out'] = result
            print(request_dict['check_out'])
            bot.send_message(call.from_user.id, 'Сколько выводить предложений?')
        else:
            bot.send_message(call.from_user.id, 'Нельзя выбрать прошедшую дату')
            calendar_bot, step = DetailedTelegramCalendar().build()
            bot.send_message(call.from_user.id,
                             f"Выберите дату выезда",
                             reply_markup=calendar_bot)


@bot.message_handler(state=SurveyStates.min_price)
def min_price(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        bot.set_state(message.from_user.id, SurveyStates.max_price)
        with bot.retrieve_data(message.from_user.id) as request_data:
            request_data['min_price'] = message.text
        bot.send_message(message.from_user.id, 'Введите максимальную стоимость за сутки (руб)')
    else:
        bot.send_message(message.from_user.id, 'Необходимо ввести любое число больше нуля')


@bot.message_handler(state=SurveyStates.max_price)
def min_price(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        bot.set_state(message.from_user.id, SurveyStates.distance)
        with bot.retrieve_data(message.from_user.id) as request_data:
            request_data['max_price'] = message.text
        bot.send_message(message.from_user.id, 'Введите максимальное удаление от центра (км)')
    else:
        bot.send_message(message.from_user.id, 'Необходимо ввести любое число больше нуля')


@bot.message_handler(state=SurveyStates.distance)
def min_price(message: Message):
    if message.text.isdigit():
        bot.set_state(message.from_user.id, SurveyStates.check_in)
        with bot.retrieve_data(message.from_user.id) as request_data:
            request_data['distance'] = message.text

        calendar_bot, step = DetailedTelegramCalendar().build()
        bot.send_message(message.from_user.id,
                         f"Выберите дату заезда",
                         reply_markup=calendar_bot)
    else:
        bot.send_message(message.from_user.id, 'Необходимо ввести целое или вещественное число')


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
        bot.send_message(message.from_user.id, 'Загружать фотографии отелей?', reply_markup=markup)
        bot.set_state(message.from_user.id, SurveyStates.get_photos)
    else:
        bot.send_message(message.from_user.id, 'Необходимо ввести целое число')


@bot.callback_query_handler(state=SurveyStates.get_photos, func=lambda x: True)
def get_photo(call: CallbackQuery):
    if call.data == 'yes':
        bot.set_state(call.from_user.id, SurveyStates.amount_of_photos)
        bot.send_message(call.from_user.id, 'Какое количество фотографий? (до 10)')

    elif call.data == 'no':
        bot.set_state(call.from_user.id, SurveyStates.results)
        with bot.retrieve_data(call.from_user.id) as request_dict:
            request_dict['amount_of_photos'] = None

            display_results(user_id=call.from_user.id)


@bot.message_handler(state=SurveyStates.amount_of_photos)
def get_photo(message: Message):
    if message.text.isdigit() and int(message.text) <= 10:
        bot.set_state(message.from_user.id, SurveyStates.results)
        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['amount_of_photos'] = int(message.text)

        display_results(user_id=message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Необходимо ввести целое число от 1 до 10')


@bot.message_handler(state=SurveyStates.results)
def city_input_details(message: Message):
    bot.send_message(message.from_user.id, 'Проверьте ввод, для справки /help')


@bot.message_handler(content_types=['text'])
def echo(message: Message):
    bot.send_message(message.from_user.id, 'Проверьте ввод, для справки /help')
