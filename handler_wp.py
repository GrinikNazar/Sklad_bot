import engine
import iphone_db


def string_separate(string): # ID2233 iPhone 8 - переклейка, АКБ
    result_list = []
    space_split = string.lower().split(' - ') # ['ID2233 iPhone 8', 'переклейка, АКБ']
    id_model = space_split[0].split(' ') # ['ID2233', 'iPhone', '8']
    model = ''.join(space_split[0].split(f'{id_model[0]}')).strip() #'iPhone 8'
    parts = space_split[1].split(',') # ['переклейка', ' АКБ']
    parts = list(map(lambda x: x.strip().lower(), parts))
    for part in parts:
        db_result = iphone_db.select_desc(part)
        if db_result:
            result_list.append(f'{model} {db_result}')
    return result_list


def string_separate_brackets(string):
    dict_of_patrs = {}
    if len(string.split('(')) == 1:
        return None
    split_bracket = string.split('(')[1].split(')')[0].split(',')
    parts = list(map(lambda x: x.strip().lower(), split_bracket))
    for part in parts:
        part = part.split(' ')
        if len(part) == 1:
            number_part = 1
            key_dict_of_parts = part[0]
        else:
            number_part = int(part[-1])
            key_dict_of_parts = ' '.join(part[:-1])
        dict_of_patrs[key_dict_of_parts] = number_part

    return dict_of_patrs


def handler_wp(message, user):
    marker = ''
    d = {
        'Готові': [],
        'Клієнтські': [],
        'Не видані': []
    }

    message = message[message.index('Готові'):]

    for msg in message.split('\n'):  
        if msg in d.keys():
            marker = msg
        elif not msg:
            continue
        else:
            d[marker].append(msg)

    list_of_values = [v for value in d.values() for v in value]

    for string in list_of_values:
        iphone_db.write_db_work_progress(user, *string_separate(string))
        if string_separate_brackets(string):
            iphone_db.write_db_work_progress(user, *string_separate_brackets(string).keys(), *string_separate_brackets(string).values())

    work_progress = iphone_db.select_table_user(user)

    result_string_bot = ''
    result_string_wp = ''

    for position in work_progress:
        if position[1] < position[2]:
            result_string_bot += f'Візьми з бота: {position[0]} - {position[2] - position[1]}шт\n'
        elif position[1] > position[2]:
            result_string_wp += f'Допиши в WProgress: {position[0]} - {position[1] - position[2]}шт\n'


    return result_string_bot + result_string_wp.rstrip()


# print(string_separate('ID2233 iPhone 8 - переклейка, АКБ нова'))
# print(handler_wp(engine.maket()))
# print(string_separate_brackets('ID2233 iPhone 8 - переклейка, АКБ нова(клей акб 2, проклейка, поляр зад 3)'))
# print(string_separate_brackets('ID2233 iPhone 8 - переклейка, АКБ нова'))
