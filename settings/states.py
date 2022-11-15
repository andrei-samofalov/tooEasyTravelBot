from telebot.handler_backends import State, StatesGroup


class SurveyStates(StatesGroup):

    city_input = State()
    check_in = State()
    check_out = State()
    amount_of_suggestion = State()
    get_photos = State()
    amount_of_photos = State()
    sort = State()
    distance = State()
    max_price = State()
    min_price = State()
    results = State()


class CommandStates(StatesGroup):

    low_price = State()
    high_price = State()
    best_deal = State()
