import datetime
import gspread
import os
import conf
import random


def connect_to_excel():
    path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI/mypython-351009-5d090fd9b043.json')
    sa = gspread.service_account(filename=path)
    return sa.open(conf.work_progress_table)


# визначення попередньої дати
def previos_date():
    date_now = datetime.datetime.now()
    month_now = date_now.month
    year_now = date_now.year
    if month_now == 1:
        previos_month = 12
        previos_year = year_now - 1
    else:
        previos_month = month_now - 1
        previos_year = year_now
    date_excel = datetime.datetime(previos_year, previos_month, 1)
    return date_excel.strftime("%m-%Y")


def search_coordinate(wks):
    col_val_coord = wks.col_values(2)
    col_val_coord = list(set(col_val_coord))
    col_val_coord = [x for x in col_val_coord if x != ''] # Знаходить координати кожного користувача

    return col_val_coord
          

def get_user_score_when_came_to_point(user_id):
    user_id = str(user_id)
    now_data = datetime.datetime.date(datetime.datetime.now())
    data_string = datetime.datetime.strftime(now_data, '%m-%Y')
    wks = connect_to_excel().worksheet(data_string)
    col_val_id = wks.col_values(1)
    for i, row in enumerate(col_val_id):
        if row == user_id:
            row_values = wks.row_values(i + 1)
            break
    user_coord = row_values[1]
    user_coord = user_coord.replace('8', '2')

    return wks.acell(user_coord).value


def get_variant_string(user_name, label, end):
    variant_list = [
        f'🏵🏵🏵{user_name}🏵🏵🏵\nНе дарма ходив на роботу і вже дійшов до позначки у {label} балів!\n👍👍Так тримати👍👍',
        f'{user_name} набрав вже більше ніж {label} балів. Давай ще)',
        f'{user_name} дійшов до позначки у {label} балів! У нього зараз {end} ̶с̶а̶н̶т̶и̶м̶е̶т̶р̶і̶в̶  балів 😎'
    ]

    return random.choice(variant_list)


def compare_scores(user_name, begin_value: str, end_value: str) -> str:
    begin_value = float(begin_value.replace(',', '.'))
    end_value = float(end_value.replace(',', '.'))
    table_score_label = (100, 120, 140, 160, 180, 200)
    for label in table_score_label:
        if begin_value < label and end_value >= label:
            return get_variant_string(user_name, label, end_value)


def get_now_day() -> int: 
    now_data = datetime.datetime.date(datetime.datetime.now())
    now_data_int = int(datetime.datetime.strftime(now_data, '%d')) #цей день 

    return now_data_int


def total_scores():
    pre_date = previos_date()
    wks = connect_to_excel().worksheet(pre_date) # конект до таблиці попереднього місяця
    coordinate = search_coordinate(wks) # [D8:E8, F8:G8, H8:I8, J8:K8, L8:M8]

    score_money = {
        (100, 120): 300,
        (120, 140): 500,
        (140, 160): 700,
        (160, 180): 1000,
        (180, 200): 1500,
        (200, 1000): 2000
        }

    name_user = '1'
    total_scores = '2'
    score_dict = {}
    best_day_dict = {}
    sum_scores = {}

    for result in coordinate:
        result_coord = result.replace('8', total_scores)
        res_total_scores = round(float(wks.acell(result_coord).value.replace(',', '.')), 2)
        
        user_name_coord = result.replace('8', name_user)
        user_name = wks.acell(user_name_coord).value

        best_d = int(wks.acell(result).value)

        best_day_dict[user_name] = best_d
        score_dict[user_name] = res_total_scores

        for key, value in score_money.items():
            if res_total_scores >= key[0] and res_total_scores < key[1]:
                sum_scores[user_name] = value + best_d * 30
                break
            else:
                if best_d == 0:
                    sum_scores[user_name] = '✋'
                else:
                    sum_scores[user_name] = best_d * 30
    
    result_string_of_scores = ''
    sorted_dict_to_list_keys= sorted(score_dict, key=score_dict.get, reverse=True) # повертає ключі посортованого словника по значеннях 
    for i, key in enumerate(sorted_dict_to_list_keys):
        number_user = i + 1
        sum_money_total = sum_scores[key]
        label_position = ''
        label_position_uah = 'грн'
        if number_user == 1:
            sum_money_total += 700
            label_position = '👑'
        elif number_user == 2:
            sum_money_total += 400
            label_position = '🏅'
        if sum_money_total == '✋':
            label_position_uah = ''

        result_string_of_scores += f'{number_user}.{label_position}{key} ({score_dict[key]}-балів) (Best D.- {best_day_dict[key]}) {sum_money_total}{label_position_uah}\n'

    return result_string_of_scores.rstrip()


def main(bot, chat): #Викликати 1 числа нового місяця о 10:00 на часовій мітці
    if get_now_day() == 1:
        bot.send_message(chat, total_scores())
