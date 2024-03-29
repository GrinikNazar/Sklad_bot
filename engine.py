import time
import handler_wp
import iphone_db
import work_progress_db
import conf
import excel_score_handlen
import scores_handler
import excel_statistic


def gen_list_models_with_color(s, apple):
    ks = s.split(' ')[-1].lower()
    s = s.lower().replace(' ', '')[len(apple):-len(ks)]
    s = s.split('/')
    return list(map(lambda x: apple + x + ks, s))


def gen_list_wth_color(s, apple):
    s = s.lower().replace(' ', '')[len(apple):]
    s = s.split('/')
    return list(map(lambda x: apple + x, s))    


def circle_color_choose(availability, min_value):
    yellow = '🟡'
    blue = '🔷'
    red = '❗️'
    if availability == 0:
        return red
    elif int(availability) <= int(min_value):
        return yellow
    else:
        return blue


def remnant_part(thing_value, value, min_value):
    remnant = thing_value - value
    if thing_value - value == 0:
        return f'{circle_color_choose(remnant, min_value)} Залишилось {thing_value - value} шт! {circle_color_choose(remnant, min_value)}'
    else:
        return f'{circle_color_choose(remnant, min_value)} Залишилось {thing_value - value} шт! {circle_color_choose(remnant, min_value)}'


def search_parts_for_add_like_back_up(dict_with_parts):
    sh = conf.source_google_sheet_api(conf.source)
    for part_key, part_value in dict_with_parts.items():
        workseet = part_key
        workseet = sh.worksheet(workseet)
        for part in part_value:
            apple = part[0]
            model = part[1].lower()
            color = part[2]
            value = part[-1]
            if color == '':
                model_pat = apple + model
            else:
                color_mode = color.replace(' ', '')
                model_pat = apple + model + color_mode
                model_pat = model_pat.lower().replace(' ', '')

            for i, row in enumerate(workseet.get_all_values()):
                if model.lower() in row[0].lower().replace(' ', ''):
                    if color == '':
                        row_res = gen_list_wth_color(row[0], apple)
                    else:
                        row_res = gen_list_models_with_color(row[0], apple)
                    if  model_pat in row_res:
                        thing_value = int(row[1])
                        workseet.update_cell(i + 1, 2, thing_value + value)
                        break


def get_thing_with_color(model, model_begin, value, workseet, sheet, *args):
    apple = iphone_db.artic(model_begin)
    color_mode = args[0].replace(' ', '')
    model_pat = apple + model + color_mode
    model_pat = model_pat.lower().replace(' ', '')
    for i, row in enumerate(workseet.get_all_values()):
        if model.lower() in row[0].lower().replace(' ', ''):
            row_res = gen_list_models_with_color(row[0], apple)
            if  model_pat in row_res:
                try:
                    thing_value = int(row[1])
                except ValueError:
                    return ['Виникла помилка звязана з *', '']
                value = int(value)
                if thing_value == 0:
                    return [f'{circle_color_choose(thing_value, row[3])} {sheet} на {apple} {model} {color_mode} - закінчились! {circle_color_choose(thing_value, row[3])}', True]
                elif value > thing_value:
                    return [f'Не можна взяти більше ніж є. В наявності {thing_value} потрібна кількість {value}', False]
                else:
                    workseet.update_cell(i + 1, 2, thing_value - value)
                    ost = remnant_part(thing_value, value, row[3])

                    dict_of_wp_parts_back_up = {
                        'sheet': sheet,
                        'apple': apple,
                        'model': model,
                        'color': args[0].lower(),
                        'value': value,
                    }

                    return [f'Взяв {sheet.lower()} на {apple} {model} {args[0].lower()} - {value} шт.\n{ost}', True, [apple.lower(), model.lower(), sheet, value], dict_of_wp_parts_back_up]


def get_thing(model, model_begin, value, workseet, sheet):
    apple = iphone_db.artic(model_begin)
    model_pat = apple + model.lower()    
    for i, row in enumerate(workseet.get_all_values()):
        row_res = gen_list_wth_color(row[0], apple)
        if model_pat in row_res:
            try:
                thing_value = int(row[1])
            except ValueError:
                return ['Виникла помилка звязана з *', '']
            value = int(value)
            if thing_value == 0:
                return [f'{circle_color_choose(thing_value, row[3])} {sheet} на {apple} {model} - закінчились! {circle_color_choose(thing_value, row[3])}', True]
            elif value > thing_value:
                return [f'Не можна взяти більше ніж є. В наявності {thing_value} потрібна кількість {value}', False]
            else:
                workseet.update_cell(i + 1, 2, thing_value - value)
                ost = remnant_part(thing_value, value, row[3])

                dict_of_wp_parts_back_up = {
                    'sheet': sheet,
                    'apple': apple,
                    'model': model,
                    'color': '',
                    'value': value,
                }

                return [f'Взяв {sheet.lower()} на {apple} {model} - {value} шт.\n{ost}', True, [apple.lower(), model.lower(), sheet, value], dict_of_wp_parts_back_up]


def get_null_things():
    sh = conf.source_google_sheet_api(conf.source)
    sheets = iphone_db.all_sheets()
    string_of_null_list = ''
    string_of_null = '\U0000274C Все що зкінчилось \U0000274C' + '\n'

    for wks in sheets:
        if wks[0] == 'Кришки':  # не показувати кришки в списку запчастин з 0
            continue
        wk = sh.worksheet(wks[0])
        title = wks[0] + ':' + '\n'
        for row in wk.get_all_values():
            if row[1] == '0':
                string_of_null_list += '- ' + row[0] + ' ' + row[1] + '\n'
        if string_of_null_list:
            string_of_null += title + string_of_null_list
        string_of_null_list = ''

    if string_of_null == '':
        return None
    else:  
        return string_of_null.rstrip()


def five(num, max_num):
    s = max_num - num
    while s % 5 != 0:
        s += 1    
    return s


def sum_parts():
    sh = conf.source_google_sheet_api(conf.source)
    sheets = iphone_db.all_sheets()
    sum_order = 0
    for wks in sheets:
        wk = sh.worksheet(wks[0])
        for number, row in enumerate(wk.get_all_values()):
            if number == 0 or row[5] == '':
                continue
            sum_order += int(row[1]) * float(row[5].replace(',', '.'))
    return sum_order


def list_ref_parts(*args):
    sh = conf.source_google_sheet_api(conf.source)
    sheets = iphone_db.all_sheets()
    sum_order = 0
    list_of_ref = []
    string_of_ref = ''
    for wks in sheets:
        wk = sh.worksheet(wks[0])
        if wks[0] == 'Додатковий':
            for row in wk.get_all_values():
                string_of_ref += row[0] + ' - ' + row[1] + '\n'
        else:
            for number, row in enumerate(wk.get_all_values()):
                if not row[4] or number == 0:
                    continue
                
                if args:
                    try:
                        if int(row[1]) <= int(row[3]):

                            if wks[1] == 'five':
                                result = five(int(row[1]), int(row[2]))
                            else:
                                result = int(row[2]) - int(row[1])
                            string_of_ref += row[4] + ' - ' + str(result) + '\n'
                            sum_order += float(row[5].replace(',', '.')) * result
                    except ValueError:
                        continue
                else:
                    try:
                        if int(row[1]) < int(row[2]):

                            if wks[1] == 'five':
                                result = five(int(row[1]), int(row[2]))
                            else:
                                result = int(row[2]) - int(row[1])
                            string_of_ref += row[4] + ' - ' + str(result) + '\n'
                            sum_order += float(row[5].replace(',', '.')) * result
                    except ValueError:
                        continue

                if len(string_of_ref) >= 4000:
                    list_of_ref.append(string_of_ref.rstrip())
                    string_of_ref = ''

    sum_order_string = f'Сумма замовлення - {round(sum_order, 2)} $'

    if string_of_ref == '':
        return None
    elif len(string_of_ref) < 4000:
        list_of_ref.append(string_of_ref.rstrip())
        list_of_ref.append(sum_order_string)
        return list_of_ref
    else:
        list_of_ref.append(sum_order_string)  
        return list_of_ref


def list_copy_and_battery(part, emod):
    sh = conf.source_google_sheet_api(conf.source)
    sheet = iphone_db.ret_uk_request(part)
    wk = sh.worksheet(sheet)
    list_order = f'{emod}{sheet}: Кількість до максимуму\n'
    for row in wk.get_all_values()[1:]:
        row_max = int(row[2])
        try:
            row_avail = int(row[1])
        except ValueError:
            continue
        if row_avail < row_max:
            list_order += f'{row[0]} - {row_max - row_avail}\n'
    return list_order.rstrip()


# Пошук всього по категорії
def search_thing(wks, sheet):
    list_result = []

    string_of_things = ''
    string_of_things += f'{sheet}\n'
    for num, row in enumerate(wks.get_all_values()):
        if num != 0:
            string_of_things += f'{num}. {row[0]} - {row[1]}\n'

        if len(string_of_things) > 4000:
            list_result.append(string_of_things.rstrip())
            string_of_things = ''

    if not list_result:
        list_result.append(string_of_things.rstrip())

    return list_result


def add_to_list(string):
    sh = conf.source_google_sheet_api(conf.source)
    workseet = sh.worksheet('Додатковий')
    string = string.split('\n')[1:]
    result_list = [f'{row[0]}*{row[1]}' for row in workseet.get_all_values()]
    result_list += string

    for i, value in enumerate(result_list):
        workseet.update_cell(i + 1, 1, value.split('*')[0])
        workseet.update_cell(i + 1, 2, value.split('*')[1])

    return string


def clean_worksheet():
    sh = conf.source_google_sheet_api(conf.source)
    workseet = sh.worksheet('Додатковий')
    workseet.clear()


def main(command):
    sh = conf.source_google_sheet_api(conf.source)
    command = command.split('_')

    sheet = iphone_db.ret_uk_request(command[0])
    wks = sh.worksheet(sheet)

    if command[1] == 'take':
        model = command[3]
        value = command[5]
        color = command[4]
        model_begin = command[2]
        if color == 'nocolor':
            result = get_thing(model, model_begin, value, wks, sheet)
        else:
            result = get_thing_with_color(model, model_begin, value, wks, sheet, color, command[0])
    else:
        result = search_thing(wks, sheet)

    return result


def handler_confirm_data(bot, users_null_list):
    message = '🔴Скинь WorkProgress🔴'
    for user in users_null_list:
        bot.send_message(user, message)


def main_time(time_b, bot, target):
    def time_mod(tm):
        time_b_list = tm.split(':')
        time_b_list = list(map(lambda x: int(x), time_b_list))
        result = (time_b_list[0] * 60) * 60 + time_b_list[1] * 60 + time_b_list[2]
        return result

    def sleep_time(start_time, end_time):
        result = end_time - start_time
        if result < 0:
            result = result * -1
            s_tome_min = (24 * 60) * 60
            result = s_tome_min - result
        return result

    def str_time_t():
        t = time.time()
        t = time.localtime(t)
        t = time.strftime('%H:%M:%S', t)
        return t

    t = str_time_t()

    while True:
        time_sleep = sleep_time(time_mod(t), time_mod(time_b))
        time.sleep(time_sleep)
        if target == 'null_time':
            excel_statistic.main(bot, conf.сhat_work_progress) # статистика кожного 1 числа нового місяця
            bot.send_message(conf.chat_history_parts, get_null_things())
            list_of_reserved_message_users = iphone_db.select_reserv_users()
            for message_reserved in list_of_reserved_message_users:
                user_name = message_reserved[0]
                message = message_reserved[1]
                message_build = user_name + '\n' + message
                bot.send_message(conf.chat_history_parts, message_build)
                iphone_db.clear_reserv(user_name)
        elif target == 'reset_time':
            excel_score_handlen.best_of_day()
            list_null_confirm = iphone_db.get_users_where_confirm_null()
            if list_null_confirm:
                for user_id in list_null_confirm:
                    scores_handler.main_scores(user_id)
                    reserv = work_progress_db.select_work_progress(user_id) # витягнути останню інформацію з макета
                    bot_name = f'@{bot.get_me().username} _wp\n' + reserv
                    reserv_result = handler_wp.handler_wp(bot_name, user_id)
                    if reserv_result:
                        iphone_db.write_reserv(user_id, reserv_result) # покласт її в резерв
            work_progress_db.reset_data_base()
        elif target == 'wp_reminder':
            handler_confirm_data(bot, iphone_db.get_users_where_confirm_null())
        elif target == 'wp_reminder_2':
            handler_confirm_data(bot, iphone_db.get_users_where_confirm_null())
        time.sleep(60)
        t = str_time_t()
