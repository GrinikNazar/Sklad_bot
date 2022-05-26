import gspread
import os

path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI\mypython-351009-5d090fd9b043.json')

sa = gspread.service_account(filename=path)

sh = sa.open('Test')

wks = sh.worksheet('Кришки')

def switch_sheet(command, content):
    content = content.split('\n')
    command = command.split('_')
    if command[0] == 'cover':
        search_covers()

#Отримуєє всі кришки які закінчились
def get_cover_null():
    string_of_covers_null = ''
    for row in wks.get_all_values():
        if row[1] == '0':
            string_of_covers_null += row[0] + ' ' + row[1] + '\n'
    if string_of_covers_null == '':
        return None
    else:  
        return string_of_covers_null.rstrip()

#Функція яка описує що користувач взяв кришку
def get_cover(value_user):
    for i, row in enumerate(wks.get_all_values()):
        if (value_user[:-2].lower() in row[0].lower()) or (value_user[:-2].lower().replace(' ', '') in row[0].lower().replace(' ', '')):
            number = int(value_user[-1])
            cover = int(row[1])
            wks.update_cell(i + 1, 2, cover - number)
    return [f'взяв кришку на {value_user[:-2]} - {number} шт ', f'Залишилось {cover - number} кришок!']


#Пошук кришок
def search_covers(search_cover, sheet):
    tuple_of_colors = (
        'gold', 'graphite', 'pasific', 'silver', 
        'black', 'blue', 'purple', 'red', 'white', 'green',
        'midnight', 'space', 'yellow', 'coral'
    )
    string_of_covers = ''
    for num, row in enumerate(sheet.get_all_values()):
        if num == 0:
            continue
        modify_string = row[0].lower().split()
        for number, model in enumerate(modify_string):
            if model in tuple_of_colors:
                modify_string = modify_string[1:number]
                break
        if str(search_cover.lower()).split() == modify_string:
            string_of_covers += f'{row[0]}, {row[1]} шт\n'

    return string_of_covers.rstrip()


#Добавити кришки
def add_cover(list_of_cover):
    for cover in list_of_cover:
        for i, row in enumerate(wks.get_all_values()):
            if cover[:-2].lower() in row[0].lower():
                number = int(cover[-1])
                wks.update_cell(i + 1, 2, int(row[1]) + number)
