import datetime
import gspread
import os
import conf
from collections import OrderedDict
# import iphone_db


def connect_to_excel():
    path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI/mypython-351009-5d090fd9b043.json')
    sa = gspread.service_account(filename=path)
    # wks = sh.worksheet('Example')
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


def get_user_score_when_came_to_point():
    pass


def get_now_day() -> int: 
    now_data = datetime.datetime.date(datetime.datetime.now())
    # data_string = datetime.datetime.strftime(now_data, '%m-%Y') #вибір назви нового листа
    now_data_int = int(datetime.datetime.strftime(now_data, '%d')) #цей день 

    return now_data_int


def main():
    # Виводити на початку нового місяця статистику по балах за попередній місяць
    # 1 та 2 місце
    # всю інформацію по бестах там де не 0
    
    pre_date = previos_date()
    wks = connect_to_excel().worksheet(pre_date) # конект до таблиці попереднього місяця
    coordinate = search_coordinate(wks) # [D8:E8, F8:G8, H8:I8, J8:K8, L8:M8]

    name_user = '1'
    total_scores = '2'
    result_string = 'Загальна кількість балів: \n'
    score_dict = {}
    string_of_best = ''

    for result in coordinate:
        result_coord = result.replace('8', total_scores)
        res_total_scores = round(float(wks.acell(result_coord).value.replace(',', '.')), 2)
        
        user_name_coord = result.replace('8', name_user)
        user_name = wks.acell(user_name_coord).value

        score_dict[user_name] = res_total_scores
    
    result_string_of_scores = ''
    sorted_dict_to_list_keys= sorted(score_dict, key=score_dict.get, reverse=True) # повертає ключі посортованого словника по значеннях 
    for i, key in enumerate(sorted_dict_to_list_keys):
        result_string_of_scores += f'{i + 1}. {key} - {score_dict[key]}\n'

    return result_string_of_scores


us_s = main()


print(us_s)

    # for i, v in us_s.items():
#     print(i, v)

