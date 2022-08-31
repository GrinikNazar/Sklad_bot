import datetime
import gspread
import os
import conf
import iphone_db

path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI/mypython-351009-5d090fd9b043.json')

sa = gspread.service_account(filename=path)

sh = sa.open(conf.score_table_change)

wks = sh.worksheet('Таблиця оцінок v2.0')

row_models = 1
first_collum = 'jobs'
list_row_models = wks.row_values(row_models)[1:]
list_row_models = list(map(lambda x: x.lower(), list_row_models))
list_row_models.insert(0, first_collum)

count_rows = wks.col_values(1) #62

print(len(count_rows))
print(list_row_models)
