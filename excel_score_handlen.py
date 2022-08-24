import datetime
import gspread
import os
import conf

path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI/mypython-351009-5d090fd9b043.json')

sa = gspread.service_account(filename=path)

sh = sa.open(conf.work_progress_table)

wks = sh.worksheet('Example') #лист приклад для копіювання| цей лист завжди однаковий і береться як зразок

now_data = datetime.datetime.date(datetime.datetime.now())
data_string = datetime.datetime.strftime(now_data, '%m-%Y') #вибір назви нового листа
now_data_int = int(datetime.datetime.strftime(now_data, '%d')) #цей день 

try:
    wks_now = sh.worksheet(data_string)
except gspread.exceptions.WorksheetNotFound:
    wks.duplicate(new_sheet_name=data_string)
    wks_now = sh.worksheet(data_string)

coordinate = {
    (1, 6, 11, 16, 21, 26, 31): ['C', 'D', 'E', 'F', 'G'], 
    (2, 7, 12, 17, 22, 27): ['I', 'J', 'K', 'L', 'M'],
    (3, 8, 13, 18, 23, 28): ['O', 'P', 'Q', 'R', 'S'],
    (4, 9, 14, 19, 24, 29): ['U', 'V', 'W', 'X', 'Y'],
    (5, 10, 15, 20, 25, 30): ['AA', 'AB', 'AC', 'AD', 'AE']}

step = 12
date_d = {
    (1, 2, 3, 4, 5) : 0, 
    (6, 7, 8, 9, 10) : step, 
    (11, 12, 13, 14, 15): 2*step,
    (16, 17, 18, 19, 20): 3*step,
    (21, 22, 23, 24, 25): 4*step,
    (26, 27, 28, 29, 30): 5*step,
    (31,): 6*step,
    }


def wks_coorditnate(id_user, now_data_int):
    row_user_id = 1
    col_values_users = wks_now.col_values(1)
    for row in col_values_users:
        if row == str(id_user):
            row_user_id += col_values_users.index(row)
            break

    #дізнаємось рядок відповідно до дати
    for key, value in date_d.items():
        if now_data_int in key:
            row_user_id += value
            break

    list_of_coordinate = []
    for key, value in coordinate.items():
        if now_data_int in key:
            for i in value:
                list_of_coordinate.append(i + str(row_user_id))
            break

    return list_of_coordinate


def main_excel(user_id, score_tuple):
    for ind, coor in enumerate(wks_coorditnate(user_id, now_data_int)):
        wks_now.update(coor, score_tuple[ind])