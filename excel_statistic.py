import datetime
import gspread
import os
import conf
# import iphone_db


def connect_to_excel():
    path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI/mypython-351009-5d090fd9b043.json')
    sa = gspread.service_account(filename=path)
    # wks = sh.worksheet('Example')
    return sa.open(conf.work_progress_table)


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


def search_coordinate():
    wks = connect_to_excel().worksheet(previos_date())

    col_val_coord = wks.col_values(2)
    col_val_coord = list(set(col_val_coord))
    col_val_coord = [x for x in col_val_coord if x != ''] # Знаходить координати кожного користувача

    return col_val_coord


def main():
    path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI/mypython-351009-5d090fd9b043.json')
    sa = gspread.service_account(filename=path)
    sh = sa.open(conf.work_progress_table)
    wks = sh.worksheet('Example')

    now_data = datetime.datetime.date(datetime.datetime.now())
    data_string = datetime.datetime.strftime(now_data, '%m-%Y') #вибір назви нового листа
    now_data_int = int(datetime.datetime.strftime(now_data, '%d')) #цей день 

    return data_string


print(search_coordinate())