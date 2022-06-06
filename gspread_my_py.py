import gspread
import iphone_db
import os

path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI\mypython-351009-5d090fd9b043.json')

sa = gspread.service_account(filename=path)

sh = sa.open('Test') #відкриває файл таблиці

# wks = sh.worksheet('') #вибір конкретного листа


#Функція яка описує що користувач взяв щось
def get_thing(model, value, workseet, sheet):
    for i, row in enumerate(workseet.get_all_values()):
        if  'iPhone' + model == row[0].replace(' ', ''):
            thing_value = int(row[1])
            value = int(value)
            workseet.update_cell(i + 1, 2, thing_value - value)
            return f'Взяв {sheet} на iPhone {model} - {value} шт.\nЗалишилось {thing_value - value} шт!'


def main(command):
    #akb_take_6_6_nocolor_1
    command = command.split('_')
    #del command[2] # - nocolor
    
    #['akb', 'take', '6', '6s', 'nocolor', '1']
    #[0] akb - з якого листа
    #[1] take - що зробити
    #[3] 6 - це група моделей, пункт не важливий
    #[4] 6s - конкретна модель
    #[5] 1 - кількість
    model = command[3]
    value = command[5]

    sheet = iphone_db.ret_uk_request(command[0])
    wks = sh.worksheet(sheet) #вибрали лист
    result = get_thing(model, value, wks, sheet)

    return result

# print(main('akb_take_6_6_nocolor_1'))

#Отримуєє все що закінчилось
def get_cover_null():
    sheets = iphone_db.all_sheets()
    string_of_null_list = ''
    string_of_null = '\U0000274C Все що зкінчилось \U0000274C' + '\n'

    for wks in sheets:
        wk = sh.worksheet(wks[0])
        string_of_null += wks[0] + ':' + '\n'
        for row in wk.get_all_values():
            if row[1] == '0':
                string_of_null_list += '- ' + row[0] + ' ' + row[1] + '\n'
        if string_of_null_list:
            string_of_null += string_of_null_list
        else:
            string_of_null += 'Все є!' + '\n'
        string_of_null_list = ''

    if string_of_null == '':
        return None
    else:  
        return string_of_null.rstrip()


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

