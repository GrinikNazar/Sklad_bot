import datetime
import gspread
import conf
import iphone_db


def get_path_and_worksheet():
    sh = conf.source_google_sheet_api(conf.work_progress_table)
    wks = sh.worksheet('Example')

    return {'wks': wks, 'sh': sh}


def max_record(wks, wks_now):
    record_cell = 'X7'

    rec_now = wks_now.acell(record_cell).value
    rec_now_float = float(rec_now.replace(',', '.'))

    rec_ex = wks.acell(record_cell).value
    rec_ex_folat = float(rec_ex.replace(',', '.'))

    if rec_now_float > rec_ex_folat: # якщо рекорд на поточному листі більший то занести його в екземпл
        wks.update_acell(record_cell, rec_now)


def get_wks_now():
    wks = get_path_and_worksheet()['wks']

    now_data = datetime.datetime.date(datetime.datetime.now())
    data_string = datetime.datetime.strftime(now_data, '%m-%Y') #вибір назви нового листа
    now_data_int = int(datetime.datetime.strftime(now_data, '%d')) #цей день 

    try:
        sh = get_path_and_worksheet()['sh']
        wks_now = sh.worksheet(data_string)
    except gspread.exceptions.WorksheetNotFound:
        wks_now = wks.duplicate(new_sheet_name=data_string)

        col_val_coord = wks.col_values(2)
        col_val_coord = list(set(col_val_coord))
        col_val_coord = [x for x in col_val_coord if x != ''] # Знаходить координати кожного користувача

        number_coord = '7'
        for coord in col_val_coord:
            coord_1 = coord[0] # D
            coord_finnaly = coord.replace('8', number_coord) #'D8:E8' > 'D7:D7' 
            example_formula = f"=ОКРУГЛ({coord_1}6*100/'{data_string}'!{coord_1}6;1)"
            wks.update_acell(coord_finnaly, value=example_formula) # запис в Example формулу з назвою поточного місяця

        wks_now.update_acell('X7', value="=ЕСЛИ(Y7 > Example!X7; Y7; Example!X7)")

    return now_data_int, wks_now
       
        
def wks_coorditnate(id_user, now_data_int, wks_now):
    coordinate = {
    (1, 6, 11, 16, 21, 26, 31): ['D', 'E', 'F', 'G', 'H'], 
    (2, 7, 12, 17, 22, 27): ['J', 'K', 'L', 'M', 'N'],
    (3, 8, 13, 18, 23, 28): ['P', 'Q', 'R', 'S', 'T'],
    (4, 9, 14, 19, 24, 29): ['V', 'W', 'X', 'Y', 'Z'],
    (5, 10, 15, 20, 25, 30): ['AB', 'AC', 'AD', 'AE', 'AF']
    }

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


def best_of_day():
    tuple_wks = get_wks_now()
    wks = tuple_wks[1]
    now_data_int = tuple_wks[0]
    begin_value = 9
    step = 6
    coordinate_of_best_day = {
        (1, 6, 11, 16, 21, 26, 31): begin_value, 
        (2, 7, 12, 17, 22, 27): begin_value + step,
        (3, 8, 13, 18, 23, 28): begin_value + step * 2,
        (4, 9, 14, 19, 24, 29): begin_value + step * 3,
        (5, 10, 15, 20, 25, 30): begin_value + step * 4
    }

    count_users = len(iphone_db.select_hose()) - 1 # мінус 1 тому що Ваня
    start_step = 11
    step = 12
    date_range_best = {
        (1, 2, 3, 4, 5) : (start_step, start_step + count_users), #два числа - 1:початок діапазону - 2:кінець
        (6, 7, 8, 9, 10) : (start_step + step, start_step + step + count_users), 
        (11, 12, 13, 14, 15): (start_step + step * 2, start_step + step * 2 + count_users),
        (16, 17, 18, 19, 20): (start_step + step * 3, start_step + step * 3 + count_users),
        (21, 22, 23, 24, 25): (start_step + step * 4, start_step + step * 4 + count_users),
        (26, 27, 28, 29, 30): (start_step + step * 5, start_step + step * 5 + count_users),
        (31,): (start_step + step * 6, start_step + step * 6 + count_users),
    }

    #треба дізнатись координати відповідно до дати
    for key, value in coordinate_of_best_day.items():
        if now_data_int in key:
            value_collum_search = value
            break

    for key, value in date_range_best.items():
        if now_data_int in key:
            diapason_tuple = value
            break

    start_value, end_value = diapason_tuple
    result_dict = {}
    for i in range(start_value, end_value):
        row_list = wks.row_values(i)
        row_list_score = row_list[value_collum_search - 1].replace(',', '.')
        score_float = float(row_list_score)
        result_dict[row_list[1]] = score_float
    
    max_dict = max(result_dict.values())
    if max_dict == 0:
        return
    for key, value in result_dict.items():
        if value == max_dict:
            end_coordinate = key
            val = int(wks.acell(end_coordinate).value)
            wks.update(end_coordinate, val + 1)


def main_excel(user_id, score_tuple):
    now_data_int, wks_now = get_wks_now()

    coordinate = wks_coorditnate(user_id, now_data_int, wks_now) #список з координатами

    for ind, coor in enumerate(coordinate):
        wks_now.update(coor, score_tuple[ind])

    max_record(get_path_and_worksheet()['wks'], wks_now)
    