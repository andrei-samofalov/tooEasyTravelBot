import json


def new_user(user_id):
    log = {'id': user_id, 'requests': []}
    return log


def load_to_dict(user_dict, command, time, data_list):
    user_dict['requests'] += {'Команда': command, 'Дата и время вызова': time, 'Результат': '\n'.join(data_list)},
    return user_dict


def load_to_json(user_id, user_dict: dict):
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



