import json


def new_user(user_id: str | int) -> dict:
    """
    Функция для создания словаря-заготовки с ID пользователя для внесения в БД
    :param user_id: str | int, ID пользователя в Телеграм
    :return: dict, словарь-заготовка для записи в базу данных
    """
    log = {'id': user_id, 'requests': []}
    return log


def collected_data(survey_dict: dict) -> str:
    """ Функция для записи собранных данных опроса """
    display = []
    for k, v in survey_dict.items():
        if k != ('destination_id' or 'current_state' or 'msg_to_delete'):
            display.append(f'{k}: {v}')
    return '\n'.join(display)


def load_to_dict(user_dict: dict, command: str, time: str, data_list: list) -> dict:
    """
    Функция для записи запрошенных отелей в словарь, созданный в функции new_user

    :param user_dict: dict, из new_user
    :param command: str, команда, которую пользователь вызвал
    :param time: str, строковое представление времени вызова команды
    :param data_list: list, данные, полученные от API
    :return: dict
    """
    user_dict['requests'] += {'Детали запроса': command,
                              'Дата и время вызова': time,
                              'Результат': '\n'.join(data_list)
                              },
    return user_dict


def load_to_json(user_id: str | int, user_dict: dict) -> None:
    """
    Функция для дампа данных из словаря user_dict в json-файл
    :param user_id: str | int, ID пользователя Телеграм
    :param user_dict: dict, словарь с собранными данными
    :return: None
    """
    try:
        with open('database/data_base.json', 'r', encoding='utf-8') as db:
            json_db = json.load(db)
    except json.decoder.JSONDecodeError:
        with open('database/data_base.json', 'w', encoding='utf-8') as db:
            data_to_dump = [user_dict]
            json.dump(data_to_dump, db, indent=4)
    else:
        with open('database/data_base.json', 'w', encoding='utf-8') as db:
            for user in json_db:
                if user['id'] == user_id:
                    for elem in user_dict['requests']:
                        user['requests'] += elem,
                    break
            else:
                json_db += user_dict,

            json.dump(json_db, db, indent=4)
