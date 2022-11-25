from telebot.types import CallbackQuery, Message
from telegram_bot_calendar import DetailedTelegramCalendar
from loader import bot

from API.get_info import city_search, is_valid_date, display_results
from bot_interface.custom_functions import format_date
from bot_interface.keyboards.inline_keyboard import inline_keyboard
from settings.states import SurveyStates
from settings.config import MAX_PHOTOS, MAX_HOTELS, NUM_ERROR, INT_ERROR


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def city_input(message: Message) -> None:
    """ Хэндлер, реагирует на команды 'lowprice', 'highprice', 'bestdeal'
        запрашивает у пользователя искомый населенный пункт """
    bot.reset_data(message.from_user.id)
    bot.send_message(message.from_user.id, 'Введите название города')
    bot.set_state(message.from_user.id, SurveyStates.city_input)
    with bot.retrieve_data(message.from_user.id) as request_dict:
        request_dict['command'] = message.text


@bot.message_handler(state=SurveyStates.city_input)
def city_input_clarify(message: Message) -> None:
    """ Хэндлер, реагирует на введенное пользователем слово, обозначающее
        населенный пункт. Отправляет запрос API city_search
        Если получает валидный результат, предлагает пользователю выбрать
        наиболее подходящий вариант
        """
    dict_of_cities = city_search(message.text)
    if dict_of_cities:
        markup = inline_keyboard(states=dict_of_cities, row_width=1)
        bot.send_message(
            chat_id=message.from_user.id,
            text='Уточните запрос',
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
    """ Хэндлер, реагирует на нажитие inline-кнопки с выбором наиболее
        подходящего населенного пункта.
        В зависимости от выбранной команды запрашивает либо минимальную
        стоимость проживания (начало ответвления опроса bestdeal),
        либо дату заезда
        """
    with bot.retrieve_data(call.from_user.id) as request_dict:
        request_dict['destination_id'] = int(call.data)
        if request_dict['command'] == '/bestdeal':
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
    result, key, step = DetailedTelegramCalendar().process(call.data)
    if not result and key:
        bot.edit_message_text(text="Выберите дату заезда",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=key)
    elif is_valid_date(result):
        bot.edit_message_text(
            text=f"Выбранная дата заезда: {format_date(result)}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.set_state(call.from_user.id, SurveyStates.check_out)
        with bot.retrieve_data(call.from_user.id) as request_dict:
            request_dict['check_in'] = result

        calendar_bot, step = DetailedTelegramCalendar().build()
        bot.send_message(chat_id=call.from_user.id,
                         text="Выберите дату выезда",
                         reply_markup=calendar_bot)
    else:
        bot.edit_message_text(
            text='Можно выбрать дату, начиная с завтрашней',
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)

        calendar_bot, step = DetailedTelegramCalendar().build()
        bot.send_message(chat_id=call.from_user.id,
                         text="Выберите дату заезда",
                         reply_markup=calendar_bot)


@bot.callback_query_handler(state=SurveyStates.check_out,
                            func=DetailedTelegramCalendar.func())
def calendar_out(call: CallbackQuery) -> None:
    """ Хэндлер, календарь для выбора даты выезда
        запрашивает количество предложений, которые необходимо отобразить
        """
    result, key, step = DetailedTelegramCalendar().process(call.data)
    with bot.retrieve_data(call.from_user.id) as request_dict:

        if not result and key:
            bot.edit_message_text(text="Выберите дату выезда",
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=key)
        elif is_valid_date(result) and result > request_dict['check_in']:
            bot.edit_message_text(
                text=f"Выбранная дата выезда: {format_date(result)}",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id)

            bot.set_state(call.from_user.id, SurveyStates.amount_of_suggestion)
            request_dict['check_out'] = result

            bot.send_message(chat_id=call.from_user.id,
                             text=f'Сколько выводить предложений '
                                  f'(максимум {MAX_HOTELS})?')
        else:
            bot.edit_message_text(text='Дата выезда может быть не ранее даты заезда '
                                       'плюс один день',
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)

            calendar_bot, step = DetailedTelegramCalendar().build()
            bot.send_message(chat_id=call.from_user.id,
                             text="Выберите дату выезда",
                             reply_markup=calendar_bot)


@bot.message_handler(state=SurveyStates.min_price)
def min_price(message: Message) -> None:
    """ Хэндлер, часть опроса bestdeal, реагирует на введенную
        минимальную стоимость, запрашивает максимальную стоимость за сутки
        """
    if message.text.isdigit() and int(message.text) > 0:
        bot.set_state(message.from_user.id, SurveyStates.max_price)
        with bot.retrieve_data(message.from_user.id) as request_data:
            request_data['min_price'] = message.text
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
            request_data['max_price'] = message.text
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
            request_data['distance'] = message.text

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
    if message.text.isdigit() and int(message.text) <= MAX_HOTELS:
        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['amount_of_suggestion'] = message.text
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
    if call.data == 'yes':
        bot.set_state(call.from_user.id, SurveyStates.amount_of_photos)
        bot.send_message(chat_id=call.from_user.id,
                         text=f'Какое количество фотографий? (до {MAX_PHOTOS})')

    elif call.data == 'no':

        # with bot.retrieve_data(call.from_user.id) as request_dict:
        #     request_dict['amount_of_photos'] = None

        display_results(user_id=call.from_user.id)
        bot.delete_state(call.from_user.id)


@bot.message_handler(state=SurveyStates.amount_of_photos)
def get_photo_amount(message: Message) -> None:
    """ Хэндлер, реагирует на введенное количество фотографий,
        запускает функцию display_results
        """
    if message.text.isdigit() and int(message.text) <= MAX_PHOTOS:

        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['amount_of_photos'] = int(message.text)

        display_results(user_id=message.from_user.id)
        bot.delete_state(message.from_user.id)

    else:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'{INT_ERROR} до {MAX_PHOTOS} включительно')


@bot.message_handler(content_types=['text'], state=SurveyStates.echo)
def echo(message: Message) -> None:
    """ Хэндлер, реагирует на любые сообщения пользователя вне опроса
        """
    bot.send_message(chat_id=message.from_user.id,
                     text='Проверьте ввод, для справки /help')
