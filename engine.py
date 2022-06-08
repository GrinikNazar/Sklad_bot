from operator import mod
import gspread
import iphone_db
import os

path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI\mypython-351009-5d090fd9b043.json')

sa = gspread.service_account(filename=path)

sh = sa.open('Test') #відкриває файл таблиці

#Функція яка описує що користувач взяв щось
def get_thing(model, value, workseet, sheet, *args):
    if args:
        if 'se' in model.lower():
            model = model[1:]
        iphone = 'iphone'
        model_pat = iphone + model + args[0]
        model_pat = model_pat.lower().replace(' ', '') #iphone8spacegray
        for i, row in enumerate(workseet.get_all_values()):
            if model.lower() in row[0].lower().replace(' ', ''):
                row_res = row[0].lower().replace(' ', '')
                row_res = row_res[:-len(args[0])]
                row_res = list(map(lambda x: iphone + x.replace(' ', '') + args[0].lower(), row_res[len(iphone):].split('/')))
                if  model_pat in row_res:
                    thing_value = int(row[1])
                    if thing_value == 0:
                        return f'🔴 {sheet} на {iphone} {model} {args[0]} - закінчились! 🔴'
                    else:
                        value = int(value)
                        workseet.update_cell(i + 1, 2, thing_value - value)
                        return f'Взяв {sheet} на iPhone {model} - {value} шт.\nЗалишилось {thing_value - value} шт!'
    else:
        if 'se' in model.lower():
            model = model[1:]
        iphone = 'iphone'
        model_pat = iphone + model.lower()    
        for i, row in enumerate(workseet.get_all_values()):
            row_res = row[0].lower().replace(' ', '')
            row_res = list(map(lambda x: iphone + x.replace(' ', ''), row_res[len(iphone):].split('/')))
            if  model_pat in row_res:
                thing_value = int(row[1])
                if thing_value == 0:
                    return f'🔴 {sheet} на {iphone} {model} - закінчились! 🔴'
                else:
                    value = int(value)
                    workseet.update_cell(i + 1, 2, thing_value - value)
                    return f'Взяв {sheet} на iPhone {model} - {value} шт.\nЗалишилось {thing_value - value} шт!'


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


#Пошук всього по категорії
def search_thing(wks, sheet):
    string_of_things = ''
    string_of_things += f'{sheet}\n'
    for num, row in enumerate(wks.get_all_values()):
        if num != 0:
            string_of_things += f'{num}. {row[0]} - {row[1]}\n'
  
    return string_of_things.rstrip()


def main(command):
    command = command.split('_')
    #['akb', 'take', '6', '6s', 'nocolor', '1']
    #[0] akb - з якого листа
    #[1] take - що зробити
    #[2] 6 - це група моделей, пункт не важливий
    #[3] 6s - конкретна модель
    #[4] nocolor - колір\без кольору
    #[5] 1 - кількість

    sheet = iphone_db.ret_uk_request(command[0]) #назва листа
    wks = sh.worksheet(sheet) #вибрали лист

    if command[1] == 'take':
        model = command[3]
        value = command[5]
        color = command[4]
        #взяти щось
        if color == 'nocolor':
            result = get_thing(model, value, wks, sheet)
        else:
            result = get_thing(model, value, wks, sheet, color, command[0])
    else:
        result = search_thing(wks, sheet)

    return result

# print(main('backlight_take_7_7_Вкладиш_1'))
# print(main('akb_take_8_8se2020_nocolor_1'))
