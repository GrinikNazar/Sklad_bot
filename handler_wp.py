import engine
import iphone_db
import work_progress_db


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


#Витягує кількісь скла з повідомлення яке скидають в work_progress
def get_count_glass_replace(message):
    message = message.split('\n')[1]
    count_glass = message.split('-')[-1]
    if count_glass == ' ':
        return 0
    else:
        return int(count_glass[-1])


#формує список з повідомлення
def wp_handler_text(message):
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

    return list_of_values


def dict_wp_compare(list_compare):
    result_dict = {}
    for string in list_compare:
        number = 1
        result_separate = string_separate(string)
        if result_separate:
            for string_result_separate in result_separate:
                if string_result_separate in result_dict.keys():
                    result_dict[string_result_separate] += number
                else:
                    result_dict[string_result_separate] = number

        #тільки в дужках
        result_separate_brackets = string_separate_brackets(string)
        if result_separate_brackets:
            for key, value in result_separate_brackets.items():
                if key in result_dict.keys():
                    result_dict[key] += value
                else:
                    result_dict[key] = value

    return result_dict


#треба зробити повернення з функції словника позицій які не сходяться
def handler_compare(user_id, values_from_message_bot): #повинна повернути словник - різницю
    message = work_progress_db.select_work_progress(user_id) #отримуєм останнє значення з ворк прогрес бази даних
    #value_list - список з повідомлення бота
    values_from_data_base = wp_handler_text(message)

    result_dict_from_db = dict_wp_compare(values_from_data_base) 
    result_dict_from_bot = dict_wp_compare(values_from_message_bot)
    result_dict = {}

    #порівгяти два словника так щоб нові дані з бота мінусувались існуючими
    for key, value in result_dict_from_bot.items():
        if key in result_dict_from_db:
            result_dict_from_bot[key] = value - result_dict_from_db[key]
            if result_dict_from_bot[key] != 0:
                result_dict[key] = result_dict_from_bot[key]
        else:
            result_dict[key] = value

    return result_dict
    


def handler_wp(message, user):
# def handler_wp(user):

    # message = work_progress_db.select_work_progress(user)

    count_glass_replace = get_count_glass_replace(message)
    work_progress_db.write_glass_count(user, count_glass_replace)
    count_glass = 'Скло'

    list_of_values = wp_handler_text(message)
    dict_handler_compare = handler_compare(user, list_of_values)

    for key, value in dict_handler_compare.items():
        work_progress_db.write_db_work_progress(user, key, value)
        if count_glass in key:
            work_progress_db.write_glass_count(user, value)

    work_progress = work_progress_db.select_table_user(user)
    glass = work_progress_db.select_glass_count(user)

    if not work_progress:
        return None

    work_progress = sorted(work_progress, key=lambda wp: count_glass not in wp[0])

    # result_replace_glass = ''
    result_string_bot = ''
    result_string_wp = ''

    for position in work_progress:
        if position[1] < position[2]:
            result_string_bot += f'Візьми з бота: {position[0]} - {position[2] - position[1]}шт\n'
        elif position[1] > position[2]:
            result_string_wp += f'Допиши в WProgress: {position[0]} - {position[1] - position[2]}шт\n'

    # if glass[0] < glass[1]:
    #     result_replace_glass += f'З бота не взяв скло для переклейки - {glass[1] - glass[0]}шт\n'
    # elif glass[0] > glass[1]:
    #     result_replace_glass += f'Не дописав в WorkProgress переклейку - {glass[0] - glass[1]}шт\n'
    # elif glass[0] == glass[1]:
    #     list_glass = []
    #     result_string_wp = result_string_wp.split('\n')
    #     for gl in result_string_wp:
    #         if count_glass not in gl:
    #             list_glass.append(gl)
    #     result_string_wp = '\n'.join(list_glass)


    return result_string_bot + result_string_wp.rstrip()

# print(handler_wp(375385945))

# x = """Переклеїв екранів - 
# Видано готових - 
# Вдано клієнтських - 
# Не виданих - 

# Готові
# id111 iphone 5s - переклейка
# id554 iphone 8 - переклейка
# id3421 iphone 8 - переклейка(проклейка, клей акб)
# id325 iphone 6 - основна камера
# id1355 iphone 7 - нижній шлейф

# Клієнтські
# id554 iphone 8 - переклейка
# id3515 iphone 12 - кришка
# id245 iphone 5 - нова акб"""

# print(handler_compare(375385945, wp_handler_text(x)))