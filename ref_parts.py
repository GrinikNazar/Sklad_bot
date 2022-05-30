import gspread
import os

path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI\mypython-351009-5d090fd9b043.json')

sa = gspread.service_account(filename=path)

sh = sa.open('Копия REFparts price!')

wks = sh.worksheet('iPad iWatch')

for row in wks.get_all_values():
    print(row[2] + ' ' + f'ціна {row[14]}')

