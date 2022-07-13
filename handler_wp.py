import engine
import iphone_db


def find_bracket(string):
    if '(' in string:
        return string[:string.find('(')]
    else:
        return string


def string_separate(string): # ID2233 iPhone 8 - переклейка, АКБ
    result_list = []
    space_split = string.lower().split(' - ') # ['ID2233 iPhone 8', 'переклейка, АКБ']
    id_model = space_split[0].split(' ') # ['ID2233', 'iPhone', '8']
    model = ''.join(space_split[0].split(f'{id_model[0]}')).strip() #'iPhone 8'
    parts = find_bracket(space_split[1])
    parts = parts.split(',') # ['переклейка', ' АКБ']
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
    space_split = string.lower().split(' - ') # ['ID2233 iPhone 8', 'переклейка, АКБ']
    id_model = space_split[0].split(' ') # ['ID2233', 'iPhone', '8']
    model = ''.join(space_split[0].split(f'{id_model[0]}')).strip() #'iPhone 8'
    split_bracket = string.split('(')[1].split(')')[0].split(',')
    parts = list(map(lambda x: x.strip().lower(), split_bracket))
    for part in parts:
        part_split = part.split(' ')
        if part_split[-1].isdigit():
            number_part = int(part_split[-1])
            key_dict_of_parts = ''.join(part_split[:-1])
        else:
            key_dict_of_parts = part
            number_part = 1
        key_dict_of_parts = f'{model} {iphone_db.select_desc(key_dict_of_parts)}'
        if key_dict_of_parts in dict_of_patrs.keys():
            dict_of_patrs[key_dict_of_parts] += number_part
        else:
            dict_of_patrs[key_dict_of_parts] = number_part
    return dict_of_patrs


def get_count_glass_replace(message):
    message = message.split('\n')[1]
    count_glass = message.split('-')[-1]
    if count_glass == ' ':
        return 0
    else:
        return int(count_glass[-1])


def handler_wp(message, user):
# def handler_wp(user):

    # message = iphone_db.select_work_progress(user)

    count_glass_replace = get_count_glass_replace(message)
    iphone_db.write_glass_count(user, count_glass_replace)
    count_glass = 'Скло'

    marker = ''
    d = {
        'Готові': [],
        'Клієнтські': [],
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

    try:
        for string in list_of_values:
            result_separate = string_separate(string)
            if result_separate:
                for string_result_separate in result_separate:
                    iphone_db.write_db_work_progress(user, string_result_separate)
                    if count_glass in string_result_separate:
                        iphone_db.write_glass_count(user)
            result_separate_brackets = string_separate_brackets(string)
            if result_separate_brackets:
                for key, value in result_separate_brackets.items():
                    iphone_db.write_db_work_progress(user, key, value)
                    if count_glass in key:
                        iphone_db.write_glass_count(user, value)
    except IndexError:
        return ['Напиши нормально, Вася!', False]

    work_progress = iphone_db.select_table_user(user)
    glass = iphone_db.select_glass_count(user)

    if not work_progress:
        return None

    work_progress = sorted(work_progress, key=lambda wp: count_glass not in wp[0])

    result_replace_glass = ''
    result_string_bot = ''
    result_string_wp = ''

    for position in work_progress:
        if position[1] < position[2]:
            result_string_bot += f'Візьми з бота: {position[0]} - {position[2] - position[1]}шт\n'
        elif position[1] > position[2]:
            result_string_wp += f'Допиши в WProgress: {position[0]} - {position[1] - position[2]}шт\n'

    if glass[0] < glass[1]:
        result_replace_glass += f'З бота не взяв скло для переклейки - {glass[1] - glass[0]}шт\n'
    elif glass[0] > glass[1]:
        result_replace_glass += f'Не дописав в WorkProgress переклейку - {glass[0] - glass[1]}шт\n'
    elif glass[0] == glass[1]:
        list_glass = []
        result_string_wp = result_string_wp.split('\n')
        for gl in result_string_wp:
            if count_glass not in gl:
                list_glass.append(gl)
        result_string_wp = '\n'.join(list_glass)


    return result_replace_glass + result_string_bot + result_string_wp.rstrip()

# print(handler_wp('Ha3aVr'))