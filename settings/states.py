from telebot.handler_backends import State, StatesGroup


class SurveyStates(StatesGroup):

    city_input = State()
