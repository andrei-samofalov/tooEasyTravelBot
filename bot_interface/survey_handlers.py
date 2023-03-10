import time

from telebot.types import CallbackQuery, Message
from telegram_bot_calendar import DetailedTelegramCalendar

import bot_interface as bi
from API import city_search_v3, display_results, is_valid_date
from database import add_request_to_db
from loader import bot
from settings import (DATE_CONFIG, INT_ERROR, MAX_HOTELS, MAX_PHOTOS, MIN_NUM,
                      SurveyStates, logger)


@bot.message_handler(commands=['search'])
def city_input(message: Message) -> None:
    """ Хэндлер, начало опроса,
        запрашивает у пользователя искомый населенный пункт """

    bot.reset_data(message.from_user.id)
    bot.send_message(message.from_user.id, 'Введите название города')
    bot.set_state(message.from_user.id, SurveyStates.city_input)
    with bot.retrieve_data(message.from_user.id) as request_dict:
        request_dict['command'] = message.text

    logger.debug(f'command: {message.text}')


@bot.message_handler(state=SurveyStates.city_input)
def city_input_clarify(message: Message) -> None:
    """ Хэндлер, реагирует на введенное пользователем слово, обозначающее
        населенный пункт. Отправляет запрос API city_search
        Если получает валидный результат, предлагает пользователю выбрать
        наиболее подходящий вариант
        """

    dict_of_cities = city_search_v3(message.text)
    if dict_of_cities:
        markup = bi.inline_keyboard(states=dict_of_cities, row_width=2)
        bot.send_message(
            chat_id=message.from_user.id,
            text='Вот, что удалось найти.\nВыберите подходящий вариант '
                 'или введите новый населенный пункт.',
            reply_markup=markup
        )
    else:
        bi.trash_message(bot, message)
        bot.send_message(
            chat_id=message.from_user.id,
            text=f'По запросу "{message.text}" ничего не найдено, '
                 'попробуйте еще раз'
        )


@bot.callback_query_handler(state=SurveyStates.city_input, func=None)
def city_input_details(call: CallbackQuery) -> None:
    """ Хэндлер, реагирует на нажатие inline-кнопки с выбором наиболее
        подходящего населенного пункта.
        В зависимости от выбранной команды запрашивает либо минимальную
        стоимость проживания (начало ответвления опроса bestdeal),
        либо дату заезда
        """

    with bot.retrieve_data(call.from_user.id) as request_dict:
        request_dict['region_id'] = call.data
        request_dict['city'] = bi.city_name_extract(
            call_dict=call.json,
            id_search=call.data)
        logger.debug(f'City: {request_dict["city"]}')
        bot.edit_message_text(
            text=f"Выбранный населенный пункт: {request_dict['city']}",
            chat_id=call.from_user.id,
            message_id=call.message.message_id
        )

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
    current_state = bot.get_state(call.from_user.id)

    if not result and key:

        bot.edit_message_text(
            text=f"{DATE_CONFIG.get(current_state).get('text')}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=key)

    elif is_valid_date(result):

        bot.edit_message_text(
            text=f"Выбранная дата заезда: {bi.format_date(result)}",
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

        bot.answer_callback_query(
            callback_query_id=call.id,
            text=DATE_CONFIG.get(current_state).get('error_text'),
            show_alert=True
        )


@bot.callback_query_handler(state=SurveyStates.check_out,
                            func=DetailedTelegramCalendar.func())
def calendar_out(call: CallbackQuery) -> None:
    """ Хэндлер, календарь для выбора даты выезда
        запрашивает количество предложений, которые необходимо отобразить
        """

    with bot.retrieve_data(call.from_user.id) as request_dict:
        check_in = request_dict['check_in']

    result, key, step = DetailedTelegramCalendar().process(call.data)
    current_state = bot.get_state(call.from_user.id)

    if not result and key:

        bot.edit_message_text(
            text=f"{DATE_CONFIG.get(current_state).get('text')}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=key)

    elif is_valid_date(result) and result > check_in:

        bot.edit_message_text(
            text=f"Выбранная дата выезда: {bi.format_date(result)}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)

        bot.set_state(call.from_user.id, SurveyStates.amount_of_suggestion)
        with bot.retrieve_data(call.from_user.id) as request_dict:
            request_dict['check_out'] = result

        bot.send_message(chat_id=call.from_user.id,
                         text=f'Сколько выводить предложений?'
                              f'\n(от {MIN_NUM} до {MAX_HOTELS})')
    else:

        bot.answer_callback_query(
            callback_query_id=call.id,
            text=DATE_CONFIG.get(current_state).get('error_text'),
            show_alert=True
        )


@bot.message_handler(state=SurveyStates.amount_of_suggestion)
def get_amount(message: Message) -> None:
    """ Хэндлер, реагирует на введенное количество выводимых предложений,
        запрашивает необходимость отображения фотографий
        """
    if message.text.isdigit() and MIN_NUM <= int(message.text) <= MAX_HOTELS:
        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['hotels_amount'] = int(message.text)
        dict_of_states = {
            'Да': 'yes',
            'Нет': 'no'
        }
        markup = bi.inline_keyboard(states=dict_of_states, row_width=1)
        bot.send_message(chat_id=message.from_user.id,
                         text='Загружать фотографии отелей?',
                         reply_markup=markup)
        bot.set_state(message.from_user.id, SurveyStates.get_photos)
    else:
        bi.trash_message(bot, message)
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
        bot.edit_message_text(
            text=f'Какое количество фотографий?\n (от {MIN_NUM} до {MAX_PHOTOS})',
            chat_id=call.from_user.id,
            message_id=call.message.message_id
        )

    elif call.data == 'no':

        bot.delete_message(
            chat_id=call.from_user.id,
            message_id=call.message.message_id
        )
        bot.set_state(call.from_user.id, SurveyStates.echo)

        with bot.retrieve_data(call.from_user.id) as request_dict:
            request_dict['photos_amount'] = 0

        add_request_to_db(
            user_id=call.from_user.id,
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
            request_dict=request_dict)
        logger.info(f'Request from {call.from_user.id} recorded to DB')

        display_results(user_id=call.from_user.id, request=request_dict)


@bot.message_handler(state=SurveyStates.amount_of_photos)
def get_photo_amount(message: Message) -> None:
    """ Хэндлер, реагирует на введенное количество фотографий,
        запускает функцию display_results
        """
    if message.text.isdigit() and MIN_NUM <= int(message.text) <= MAX_PHOTOS:

        with bot.retrieve_data(message.from_user.id) as request_dict:
            request_dict['photos_amount'] = int(message.text)

        add_request_to_db(
            user_id=message.from_user.id,
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
            request_dict=request_dict)
        logger.info(f'Request from {message.from_user.id} recorded to DB')

        bot.set_state(message.from_user.id, SurveyStates.echo)
        display_results(user_id=message.from_user.id,
                        request=request_dict)

    else:
        bi.trash_message(bot, message)
        bot.send_message(chat_id=message.from_user.id,
                         text=f'{INT_ERROR} до {MAX_PHOTOS} включительно..')
