from telebot.handler_backends import State, StatesGroup


class SurveyStates(StatesGroup):
    city_input = State()
    check_in = State()
    check_out = State()
    amount_of_suggestion = State()
    get_photos = State()
    amount_of_photos = State()
    echo = State()
    history = State()
