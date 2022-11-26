from telebot.types import CallbackQuery, Message
from telegram_bot_calendar import DetailedTelegramCalendar

from API.get_info import city_search, display_results, is_valid_date
from bot_interface.custom_functions import (city_name_extract,
                                            delete_echo_messages, format_date,
                                            trash_message)
from bot_interface.error_replies import date_error
from bot_interface.keyboards.inline_keyboard import inline_keyboard
from loader import bot
from settings.config import (DATE_CONFIG, INT_ERROR, MAX_HOTELS, MAX_PHOTOS,
                             NUM_ERROR)
from settings.states import SurveyStates


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def city_input(message: Message) -> None:
    """ Хэндлер, реагирует на команды 'lowprice', 'highprice', 'bestdeal'
        запрашивает у пользователя искомый населенный пункт """
    delete_echo_messages(bot, message.from_user.id)
    # bot.reset_data(message.from_user.id)

    bot.send_message(message.from_user.id, 'Введите название города')
    bot.set_state(message.from_user.id, SurveyStates.city_input)
    with bot.retrieve_data(message.from_user.id) as request_dict:
        request_dict['Команда'] = message.text


@bot.message_handler(state=SurveyStates.city_input)
def city_input_clarify(message: Message) -> None:
    """ Хэндлер, реагирует на введенное пользователем слово, обозначающее
        населенный пункт. Отправляет запрос API city_search
        Если получает валидный результат, предлагает пользователю выбрать
        наиболее подходящий вариант
        """
    delete_echo_messages(bot, message.from_user.id)
    dict_of_cities = city_search(message.text)
    if dict_of_cities:
        markup = inline_keyboard(states=dict_of_cities, row_width=2)
        bot.send_message(
            chat_id=message.from_user.id,
            text='Вот, что удалось найти.\nВыберите подходящий вариант '
                 'или введите новый населенный пункт.',
            reply_markup=markup
        )
    else:
        bot.send_message(
            chat_id=message.from_user.id,
            text='По запросу ничего не найдено, '
                 'введите корректное название населенного пункта'
        )


@bot.callback_query_handler(state=SurveyStates.city_input, func=None)
def city_input_details(call: CallbackQuery) -> None:
    """ Хэндлер, реагирует на нажатие inline-кнопки с выбором наиболее
        подходящего населенного пункта.
        В зависимости от выбранной команды запрашивает либо минимальную
        стоимость проживания (начало ответвления опроса bestdeal),
        либо дату заезда
        """
    delete_echo_messages(bot, call.from_user.id)
    with bot.retrieve_data(call.from_user.id) as request_dict:
        request_dict['destination_id'] = int(call.data)
        request_dict['Населенный пункт'] = city_name_extract(
                                                    call_dict=call.json,
                                                    id_search=call.data)
        bot.edit_message_text(
            text=f"Выбранный населенный пункт: {request_dict['Населенный пункт']}",
            chat_id=call.from_user.id,
            message_id=call.message.message_id
        )

        if request_dict['Команда'] == '/bestdeal':
            bot.set_state(call.from_user.id, SurveyStates.min_price)
            bot.send_message(call.from_user.id,
                             'Введите минимальную стоимость за сутки (руб)')
        else:
            bot.set_state(call.from_user.id, SurveyStates.check_in)
            calendar_bot, step = DetailedTelegramCalendar().build()
            bot.send_message(chat_id=call.from_user.id,
                             text="Выберите дату заезда",
                             reply_markup=calendar_bot)


@bot.callback_query_handler(state=SurveyStates.check_in,
                            func=DetailedTelegramCalendar.func())
def calendar_in(call: CallbackQuery) -> None:
    """ Хэндлер, календарь, записывает дату заезда,
        запрашивает дату выезда
        """
    delete_echo_messages(bot, call.from_user.id)

    result, key, step = DetailedTelegramCalendar().process(call.data)
    current_state = bot.get_state(call.from_user.id)

    if not result and key:
        delete_echo_messages(bot, call.from_user.id)
        bot.edit_message_text(
            text=f"{DATE_CONFIG.get(current_state).get('text')}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=key)

    elif is_valid_date(result):
        delete_echo_messages(bot, call.from_user.id)
        bot.edit_message_text(
            text=f"Выбранная дата заезда: {format_date(result)}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.set_state(call.from_user.id, SurveyStates.check_out)
        with bot.retrieve_data(call.from_user.id) as request_dict:
            request_dict['Дата заезда'] = result

        calendar_bot, step = DetailedTelegramCalendar().build()
        bot.send_message(chat_id=call.from_user.id,
                         text="Выберите дату выезда",
                         reply_markup=calendar_bot)
    else:
        date_error(bot, call, current_state)


@bot.message_handler(state=SurveyStates.check_in)
def trash_check_in(message: Message):
    trash_message(bot, message)


@bot.message_handler(state=SurveyStates.check_out)
def trash_check_out(message: Message):
    trash_message(bot, message)


@bot.callback_query_handler(state=SurveyStates.check_out,
                            func=DetailedTelegramCalendar.func())
def calendar_out(call: CallbackQuery) -> None:
    """ Хэндлер, календарь для выбора даты выезда
        запрашивает количество предложений, которые необходимо отобразить
        """
    delete_echo_messages(bot, call.from_user.id)
    with bot.retrieve_data(call.from_user.id) as request_dict:
        check_in = request_dict['Дата заезда']

    result, key, step = DetailedTelegramCalendar().process(call.data)
    current_state = bot.get_state(call.from_user.id)

    if not result and key:
        delete_echo_messages(bot, call.from_user.id)
        bot.edit_message_text(
            text=f"{DATE_CONFIG.get(current_state).get('text')}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=key)

    elif is_valid_date(result) and result > check_in:
        delete_echo_messages(bot, call.from_user.id)
        bot.edit_message_text(
            text=f"Выбранная дата выезда: {format_date(result)}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)

        bot.set_state(call.from_user.id, SurveyStates.amount_of_suggestion)
        with bot.retrieve_data(call.from_user.id) as request_dict:
            request_dict['Дата выезда'] = result

        bot.send_message(chat_id=call.from_user.id,
                         text=f'Сколько выводить предложений '
                              f'(максимум {MAX_HOTELS})?')
    else:
        date_error(bot, call, current_state)


@bot.callback_query_handler(func=None, state=SurveyStates.date_error)
def date_error_handler(call: CallbackQuery) -> None:
    """Колбэк, ожидающий, что пользователь нажмет 'понятно'
        """
    delete_echo_messages(bot, call.from_user.id)
    with bot.retrieve_data(call.from_user.id) as request_data:

        current_state = request_data['current_state']
        del request_data['current_state']

    if call.data == 'got_it':

        bot.delete_message(chat_id=call.from_user.id,
                           message_id=call.message.message_id)

        calendar_bot, step = DetailedTelegramCalendar().build()
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"{DATE_CONFIG.get(current_state).get('text')}",
            reply_markup=calendar_bot
        )
        bot.set_state(call.from_user.id, current_state)


@bot.message_handler(state=SurveyStates.min_price)
def min_price(message: Message) -> None:
    """ Хэндлер, часть опроса bestdeal, реагирует на введенную
        минимальную стоимость, запрашивает максимальную стоимость за сутки
        """
    if message.text.isdigit() and int(message.text) > 0:
        bot.set_state(message.from_user.id, SurveyStates.max_price)
        with bot.retrieve_data(message.from_user.id) as request_data:
            request_data['Минимальная цена'] = message.text
        bot.send_message(chat_id=message.from_user.id,
                         text='Введите максимальную стоимость за сутки (руб)')
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=NUM_ERROR)


@bot.message_handler(state=SurveyStates.max_price)
def max_price(message: Message) -> None:
    """ Хэндлер, часть опроса bestdeal, реагирует на введенную
        максимальную стоимость, запрашивает максимальное удаление от центра
        """
    if message.text.isdigit() and int(message.text) > 0:
        bot.set_state(message.from_user.id, SurveyStates.distance)
        with bot.retrieve_data(message.from_user.id) as request_data:
            request_data['Максимальная цена'] = message.text
        bot.send_message(chat_id=message.from_user.id,
                         text='Введите максимальное удаление от центра (км)')
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=NUM_ERROR)


@bot.message_handler(state=SurveyStates.distance)
def get_distance(message: Message) -> None:
    """ Хэндлер, часть опроса bestdeal, реагирует на введенное
        максимальное удаление от центра, запрашивает дату заезда,
        опрос bestdeal вливается в общий опрос lowprice и highprice
        """
    if message.text.isdigit() and float(message.text) >= 0:
        bot.set_state(message.from_user.id, SurveyStates.check_in)
        with bot.retrieve_data(message.from_user.id) as request_data:
            request_data['Расстояние до центра'] = message.text

        calendar_bot, step = DetailedTelegramCalendar().build()
        bot.send_message(chat_id=message.from_user.id,
                         text="Выберите дату заезда",
                         reply_markup=calendar_bot)
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=NUM_ERROR)


@bot.message_handler(state=SurveyStates.amount_of_suggestion)
def get_amount(message: Message) -> None:
    """ Хэндлер, реагирует на введенное количество выводимых предложений,
        запрашивает необходимость отображения фотографий
        """
    delete_echo_messages(bot, message.from_user.id)
    if message.text.isdigit() and int(message.text) <= MAX_HOTELS:
        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['Кол-во предложений'] = message.text
        dict_of_states = {
            'Да': 'yes',
            'Нет': 'no'
        }
        markup = inline_keyboard(states=dict_of_states, row_width=1)
        bot.send_message(chat_id=message.from_user.id,
                         text='Загружать фотографии отелей?',
                         reply_markup=markup)
        bot.set_state(message.from_user.id, SurveyStates.get_photos)
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'{INT_ERROR} до {MAX_HOTELS} включительно')


@bot.callback_query_handler(state=SurveyStates.get_photos, func=None)
def get_photo(call: CallbackQuery) -> None:
    """ Хэндлер, реагирует на ответ да или нет вопрос о необходимости
        отображения фотографий, запускает функцию display_results, если
        получен отрицательный ответ. В случае положительного ответа пользователя
        запрашивает количество фотографий, которое необходимо выгрузить
        """
    delete_echo_messages(bot, call.from_user.id)
    if call.data == 'yes':

        bot.set_state(call.from_user.id, SurveyStates.amount_of_photos)
        bot.edit_message_text(
            text=f'Какое количество фотографий? (до {MAX_PHOTOS})',
            chat_id=call.from_user.id,
            message_id=call.message.message_id
        )

    elif call.data == 'no':
        bot.delete_message(
            chat_id=call.from_user.id,
            message_id=call.message.message_id
        )
        bot.set_state(call.from_user.id, SurveyStates.echo)
        display_results(user_id=call.from_user.id)


@bot.message_handler(state=SurveyStates.amount_of_photos)
def get_photo_amount(message: Message) -> None:
    """ Хэндлер, реагирует на введенное количество фотографий,
        запускает функцию display_results
        """
    if message.text.isdigit() and int(message.text) <= MAX_PHOTOS:

        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['Кол-во фотографий'] = int(message.text)

        bot.set_state(message.from_user.id, SurveyStates.echo)
        display_results(user_id=message.from_user.id)

    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'{INT_ERROR} до {MAX_PHOTOS} включительно')
