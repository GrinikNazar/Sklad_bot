import sqlite3
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

jobs = wks.col_values(1)

try:
    iphone_db.drop_table_from_excel()
except sqlite3.OperationalError:
    pass
iphone_db.create_table_from_excel(list_row_models)

for row_number in range(2, len(jobs)):
    row = wks.row_values(row_number)
    row = list(map(lambda x: x.lower(), row))
    iphone_db.insert_to_db_from_excel(list_row_models, row)

# TODO: робити доп варіанти через базу даних
#