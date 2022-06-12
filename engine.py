from operator import mod
import gspread
import iphone_db
import os

path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI\mypython-351009-5d090fd9b043.json')

sa = gspread.service_account(filename=path)

sh = sa.open('Test') #відкриває файл таблиці

def gen_list_models(s, apple):
    ks = s.split(' ')[-1].lower()
    s = s.lower().replace(' ', '')[len(apple):-len(ks)]
    s = s.split('/')
    return list(map(lambda x: apple + x + ks, s))

#Функція яка описує що користувач взяв щось
def get_thing(model, model_begin, value, workseet, sheet, *args):
    if args:
        apple = iphone_db.artic(model_begin)
        color_mode = args[0].replace(' ', '')
        model_pat = apple + model + color_mode
        model_pat = model_pat.lower().replace(' ', '')
        for i, row in enumerate(workseet.get_all_values()):
            if model.lower() in row[0].lower().replace(' ', ''):
                # row_res = row[0].lower().replace(' ', '')
                row_res = gen_list_models(row[0], apple)
                # color_row = row_res.split(model.lower())[-1]
                # row_res = row_res[:-len(color_row)]
                # row_res = list(map(lambda x: apple + x.replace(' ', '') + color_row.lower(), row_res[len(apple):].split('/')))
                if  model_pat in row_res:
                    thing_value = int(row[1])
                    value = int(value)
                    if thing_value == 0:
                        return [f'🔴 {sheet} на {apple} {model} {color_mode} - закінчились! 🔴', True]
                    elif value > thing_value:
                        return [f'Не можна взяти більше ніж є. В наявності {thing_value} потрібна кількість {value}', False]
                    else:
                        workseet.update_cell(i + 1, 2, thing_value - value)
                        if thing_value - value == 0:
                            ost = f'🔴 Залишилось {thing_value - value} шт! 🔴'
                        else:
                            ost = f'🔵 Залишилось {thing_value - value} шт! 🔵'
                        return [f'Взяв {sheet.lower()} на {apple} {model} {args[0].lower()} - {value} шт.\n🔵 Залишилось {thing_value - value} шт! 🔵', True]
    else:
        apple = iphone_db.artic(model_begin)
        model_pat = apple + model.lower()    
        for i, row in enumerate(workseet.get_all_values()):
            row_res = row[0].lower().replace(' ', '')
            row_res = list(map(lambda x: apple + x.replace(' ', ''), row_res[len(apple):].split('/')))
            if  model_pat in row_res:
                thing_value = int(row[1])
                value = int(value)
                if thing_value == 0:
                    return [f'🔴 {sheet} на {apple} {model} - закінчились! 🔴', True]
                elif value > thing_value:
                    return [f'Не можна взяти більше ніж є. В наявності {thing_value} потрібна кількість {value}', False]
                else:
                    workseet.update_cell(i + 1, 2, thing_value - value)
                    if thing_value - value == 0:
                        ost = f'🔴 Залишилось {thing_value - value} шт! 🔴'
                    else:
                        ost = f'🔵 Залишилось {thing_value - value} шт! 🔵'
                    return [f'Взяв {sheet.lower()} на iPhone {model} - {value} шт.\n{ost}', True]


#Отримуєє все що закінчилось
def get_null_things():
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

#список на реф
def list_ref_parts():
    sheets = iphone_db.all_sheets()
    sum_order = 0
    list_of_ref = []
    string_of_ref = ''
    for wks in sheets:
        wk = sh.worksheet(wks[0])
        for row in wk.get_all_values():
            if not row[4]:
                continue
            if row[1] <= row[3]:
                result = int(row[1]) + (int(row[2]) - int(row[1]))
                string_of_ref += row[4] + ' - ' + str(result) + '\n'

                sum_order += float(row[5].replace(',', '.'))
            if len(string_of_ref) >= 4000:
                list_of_ref.append(string_of_ref.rstrip())
                string_of_ref = ''
    
    sum_order_string = f'Сумма замовлення - {round(sum_order, 2)} $'
    
    if string_of_ref == '':
        return None
    elif len(string_of_ref) < 4000:
        list_of_ref.append(string_of_ref.rstrip())
        list_of_ref.append(sum_order_string)
        return list_of_ref
    else:
        list_of_ref.append(sum_order_string)  
        return list_of_ref


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
    #[2] 6 - це група моделей
    #[3] 6s - конкретна модель
    #[4] nocolor - колір\без кольору
    #[5] 1 - кількість

    sheet = iphone_db.ret_uk_request(command[0]) #назва листа
    wks = sh.worksheet(sheet) #вибрали лист

    if command[1] == 'take':
        model = command[3]
        value = command[5]
        color = command[4]
        model_begin = command[2]
        #взяти щось
        if color == 'nocolor':
            result = get_thing(model, model_begin, value, wks, sheet)
        else:
            result = get_thing(model, model_begin, value, wks, sheet, color, command[0])
    else:
        result = search_thing(wks, sheet)

    return result

# print(main('gluepr_take_X_X_Клей АКБ_1'))
# print(main('akb_take_8_8se2020_nocolor_1'))
# print(list_ref_parts())
