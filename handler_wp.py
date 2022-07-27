import engine
import iphone_db
import work_progress_db


def find_bracket(string):
    if '(' in string:
        return string[:string.find('(')]
    else:
        return string


#для знаходження моделі
def choose_model_parse(space_split):
    id_model = space_split[0].split(' ')
    id_model = [i for i in id_model if i != '']
    id_model.remove(id_model[0])
    model = id_model.pop(0)
    try:
        model = iphone_db.select_all_telephone_name(model)
    except IndexError:
        model = model
    id_model.insert(0, model)
    return ' '.join(id_model).strip()


def string_separate(string):
    result_list = []
    space_split = string.lower().split('-')
    model = choose_model_parse(space_split)
    parts = find_bracket(space_split[1])
    parts = parts.split(',')
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
    space_split = string.lower().split('-')
    model = choose_model_parse(space_split)
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
    

#порівняти дані
def wp_position(work_progress):
    result_string_bot = ''
    result_string_wp = ''
    for position in work_progress:
        if position[1] < position[2]:
            result_string_bot += f'Візьми з бота: {position[0]} - {position[2] - position[1]} шт\n'
        elif position[1] > position[2]:
            result_string_wp += f'Допиши в WProgress: {position[0]} - {position[1] - position[2]} шт\n'

    return result_string_bot + result_string_wp.rstrip()


#Список можливих варіантів скла для аналізу
def get_additional_list_part(result_string_glass, string_for_chek):
    bot = 'Візьми з бота'
    wp = 'Допиши в WProgress'
    result = []
    result_string_glass = result_string_glass.rstrip()
    resul_join = result_string_glass.split('\n')
    if string_for_chek == 'wp':
        for string in resul_join:
            string = string.split(': ')
            if string[0] == wp:
                result.append(string[1])
    elif string_for_chek == 'bot':
        for string in resul_join:
            string = string.split(': ')
            if string[0] == bot:
                result.append(string[1])

    resul_join = '\n'.join(result)

    if resul_join == '':
        return ''

    return f'Можливо це скло з наступного списку:\n{resul_join}\n\U0001F9A5\U0001F43E\U0001F9AB\U0001F43E\U0001F40D\U0001F40C\n'


def handler_wp(message, user):
# def handler_wp(user):
    # message = work_progress_db.select_work_progress(user)

    count_glass_replace = get_count_glass_replace(message) #кількість скла з повідомлення зверху

    list_of_values = wp_handler_text(message)
    dict_handler_compare = handler_compare(user, list_of_values)

    for key, value in dict_handler_compare.items():
        work_progress_db.write_db_work_progress(user, key, value)

    work_progress = work_progress_db.select_table_user(user)
    work_progress_glass = work_progress_db.select_table_user_glass(user) #витягнути доні по склу

    sum_bot = 0
    sum_wp = count_glass_replace
    for item in work_progress_glass:
        sum_bot += item[1]
        sum_wp += item[2]

    if not work_progress and not work_progress_glass:
        return None

    result_work_progress = wp_position(work_progress)
    result_string_glass = wp_position(work_progress_glass)

    result_glass_count = ''
    if sum_bot > sum_wp:
        result_glass_count += f'Не дописав переклейку в WorkProgress - {sum_bot - sum_wp} шт\n'
        result_string_glass = get_additional_list_part(result_string_glass, 'wp')  #тільки те що не дописав в переклейку
    elif sum_bot < sum_wp:
        result_glass_count += f'Не взяв з бота скло - {sum_wp - sum_bot} шт\n'
        result_string_glass = get_additional_list_part(result_string_glass, 'bot') #тільки те що не взяв з бота
    else:
        #дописати result_string_glass тільки те що треба взяти з бота
        finally_string_glass = ''
        for string_glass in result_string_glass.split('\n'):
            if 'Візьми з бота' in string_glass:
                finally_string_glass += string_glass + '\n'
        result_string_glass = finally_string_glass

    return result_glass_count + result_string_glass + result_work_progress.rstrip()

# print(handler_wp(375385945))
