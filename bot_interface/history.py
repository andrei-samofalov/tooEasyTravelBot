import time
from loader import bot
from telebot.types import Message
from settings.states import SurveyStates
import json


@bot.message_handler(commands=['history'])
def get_history(message: Message):
    bot.send_message(message.from_user.id, 'Какое количество последних запросов вывести?')
    bot.set_state(message.from_user.id, SurveyStates.history)


@bot.message_handler(state=SurveyStates.history)
def get_history(message: Message):

    if message.text.isdigit():
        amount = int(message.text)
        try:
            with open('database/data_base.json', 'r', encoding='utf-8') as db:
                json_db = json.load(db)
        except json.decoder.JSONDecodeError:
            bot.send_message(chat_id=message.from_user.id,
                             text='База данных еще не сформирована, сделайте свой первый запрос \n/help - справка')
        else:
            bot.delete_state(message.from_user.id)
            # bot.set_state(chat_id=message.from_user.id,
            #               state=SurveyStates.echo)
            for user in json_db:
                if user.get('id') == message.from_user.id:
                    user_requests = len(user.get('requests', []))
                    request_amount = user_requests - amount
                    if request_amount >= 0:
                        for request in user['requests'][request_amount:]:
                            display = [f'<u>{k}</u>\n{v}' for k, v in request.items()]
                            bot.send_message(chat_id=message.from_user.id, text='\n\n'.join(display),
                                             disable_web_page_preview=True)
                            time.sleep(1)
                        break
                    else:
                        bot.send_message(
                            chat_id=message.from_user.id,
                            text=f'Вы сделали меньше количество запросов, чем желаете отобразить ({user_requests})'
                        )
            else:
                bot.send_message(chat_id=message.from_user.id,
                                 text='Вы еще не делали запросов, самое время это сделать!\n/help - справка')
    else:
        bot.send_message(chat_id=message.from_user.id, text='Необходимо ввести целое число')
