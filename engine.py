import time
import gspread
import iphone_db
import os
import work_progress_db

path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI/mypython-351009-5d090fd9b043.json')

sa = gspread.service_account(filename=path)

sh = sa.open('inStyle_parts')
# sh = sa.open('Test_parts')


def gen_list_models_with_color(s, apple):
    ks = s.split(' ')[-1].lower()
    s = s.lower().replace(' ', '')[len(apple):-len(ks)]
    s = s.split('/')
    return list(map(lambda x: apple + x + ks, s))


def circle_color_choose(availability, min_value):
    yellow = '🟡'
    blue = '🔷'
    red = '❗️'
    if availability == 0:
        return red
    elif int(availability) <= int(min_value):
        return yellow
    else:
        return blue


def remnant_part(thing_value, value, min_value):
    remnant = thing_value - value
    if thing_value - value == 0:
        return f'{circle_color_choose(remnant, min_value)} Залишилось {thing_value - value} шт! {circle_color_choose(remnant, min_value)}'
    else:
        return f'{circle_color_choose(remnant, min_value)} Залишилось {thing_value - value} шт! {circle_color_choose(remnant, min_value)}'


def get_thing_with_color(model, model_begin, value, workseet, sheet, *args):
    apple = iphone_db.artic(model_begin)
    color_mode = args[0].replace(' ', '')
    model_pat = apple + model + color_mode
    model_pat = model_pat.lower().replace(' ', '')
    for i, row in enumerate(workseet.get_all_values()):
        if model.lower() in row[0].lower().replace(' ', ''):
            row_res = gen_list_models_with_color(row[0], apple)
            if  model_pat in row_res:
                thing_value = int(row[1])
                value = int(value)
                if thing_value == 0:
                    return [f'{circle_color_choose(thing_value, row[3])} {sheet} на {apple} {model} {color_mode} - закінчились! {circle_color_choose(thing_value, row[3])}', True]
                elif value > thing_value:
                    return [f'Не можна взяти більше ніж є. В наявності {thing_value} потрібна кількість {value}', False]
                else:
                    workseet.update_cell(i + 1, 2, thing_value - value)
                    ost = remnant_part(thing_value, value, row[3])

                    return [f'Взяв {sheet.lower()} на {apple} {model} {args[0].lower()} - {value} шт.\n{ost}', True, [apple.lower(), model.lower(), sheet, value]]


def gen_list_wth_color(s, apple):
    s = s.lower().replace(' ', '')[len(apple):]
    s = s.split('/')
    return list(map(lambda x: apple + x, s))


def get_thing(model, model_begin, value, workseet, sheet):
    apple = iphone_db.artic(model_begin)
    model_pat = apple + model.lower()    
    for i, row in enumerate(workseet.get_all_values()):
        row_res = gen_list_wth_color(row[0], apple)
        if  model_pat in row_res:
            thing_value = int(row[1])
            value = int(value)
            if thing_value == 0:
                return [f'{circle_color_choose(thing_value, row[3])} {sheet} на {apple} {model} - закінчились! {circle_color_choose(thing_value, row[3])}', True]
            elif value > thing_value:
                return [f'Не можна взяти більше ніж є. В наявності {thing_value} потрібна кількість {value}', False]
            else:
                workseet.update_cell(i + 1, 2, thing_value - value)
                ost = remnant_part(thing_value, value, row[3])

                return [f'Взяв {sheet.lower()} на {apple} {model} - {value} шт.\n{ost}', True, [apple.lower(), model.lower(), sheet, value]]


def get_null_things():
    sheets = iphone_db.all_sheets()
    string_of_null_list = ''
    string_of_null = '\U0000274C Все що зкінчилось \U0000274C' + '\n'

    for wks in sheets:
        wk = sh.worksheet(wks[0])
        title = wks[0] + ':' + '\n'
        for row in wk.get_all_values():
            if row[1] == '0':
                string_of_null_list += '- ' + row[0] + ' ' + row[1] + '\n'
        if string_of_null_list:
            string_of_null += title + string_of_null_list
        string_of_null_list = ''

    if string_of_null == '':
        return None
    else:  
        return string_of_null.rstrip()


def five(num, max_num):
    s = max_num - num
    while s % 5 != 0:
        s += 1    
    return s


def sum_parts():
    sheets = iphone_db.all_sheets()
    sum_order = 0
    for wks in sheets:
        wk = sh.worksheet(wks[0])
        for number, row in enumerate(wk.get_all_values()):
            if number == 0 or row[5] == '':
                continue
            sum_order += int(row[1]) * float(row[5].replace(',', '.'))
    return sum_order


def list_ref_parts(*args):
    sheets = iphone_db.all_sheets()
    sum_order = 0
    list_of_ref = []
    string_of_ref = ''
    for wks in sheets:
        wk = sh.worksheet(wks[0])
        if wks[0] == 'Додатковий':
            for row in wk.get_all_values():
                string_of_ref += row[0] + ' - ' + row[1] + '\n'
        else:
            for number, row in enumerate(wk.get_all_values()):
                if not row[4] or number == 0:
                    continue
                
                if args:
                    if int(row[1]) <= int(row[3]):

                        if wks[1] == 'five':
                            result = five(int(row[1]), int(row[2]))
                        else:
                            result = int(row[2]) - int(row[1])
                        string_of_ref += row[4] + ' - ' + str(result) + '\n'
                        sum_order += float(row[5].replace(',', '.')) * result
                else:
                    if int(row[1]) < int(row[2]):

                        if wks[1] == 'five':
                            result = five(int(row[1]), int(row[2]))
                        else:
                            result = int(row[2]) - int(row[1])
                        string_of_ref += row[4] + ' - ' + str(result) + '\n'
                        sum_order += float(row[5].replace(',', '.')) * result

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


def list_copy_and_battery(part, emod):
    sheet = iphone_db.ret_uk_request(part)
    wk = sh.worksheet(sheet)
    list_order = f'{emod[0]}{sheet}: Кількість до максимуму\n'
    num = 0
    for row in wk.get_all_values()[1:]:
        row_max = int(row[2])
        row_avail = int(row[1])
        if row_avail < row_max:
            num += 1
            list_order += f'{num}. {row[0]} - {row_max - row_avail}\n'
    return list_order.rstrip()


#Пошук всього по категорії
def search_thing(wks, sheet):
    string_of_things = ''
    string_of_things += f'{sheet}\n'
    for num, row in enumerate(wks.get_all_values()):
        if num != 0:
            string_of_things += f'{num}. {row[0]} - {row[1]}\n'
  
    return string_of_things.rstrip()


def add_to_list(string):
    workseet = sh.worksheet('Додатковий')
    string = string.split('\n')[1:]
    result_list = [f'{row[0]}*{row[1]}' for row in workseet.get_all_values()]
    result_list += string

    for i, value in enumerate(result_list):
        workseet.update_cell(i + 1, 1, value.split('*')[0])
        workseet.update_cell(i + 1, 2, value.split('*')[1])

    return string


def clean_worksheet():
    workseet = sh.worksheet('Додатковий')
    workseet.clear()


def main(command):
    command = command.split('_')

    sheet = iphone_db.ret_uk_request(command[0])
    wks = sh.worksheet(sheet)

    if command[1] == 'take':
        model = command[3]
        value = command[5]
        color = command[4]
        model_begin = command[2]
        if color == 'nocolor':
            result = get_thing(model, model_begin, value, wks, sheet)
        else:
            result = get_thing_with_color(model, model_begin, value, wks, sheet, color, command[0])
    else:
        result = search_thing(wks, sheet)

    return result

def main_time(time_b, bot, target):
    def time_mod(tm):
        time_b_list = tm.split(':')
        time_b_list = list(map(lambda x: int(x), time_b_list))
        result = (time_b_list[0] * 60) * 60 + time_b_list[1] * 60 + time_b_list[2]
        return result

    def sleep_time(start_time, end_time):
        result = end_time - start_time
        if result < 0:
            result = result * -1
            s_tome_min = (24 * 60) * 60
            result = s_tome_min - result
        return result

    def str_time_t():
        t = time.time()
        t = time.localtime(t)
        t = time.strftime('%H:%M:%S', t)
        return t

    t = str_time_t()

    while True:
        time_sleep = sleep_time(time_mod(t), time_mod(time_b))
        time.sleep(time_sleep)
        if target == 'null_time':
            bot.send_message(-674239373, get_null_things())
        elif target == 'reset_time':
            work_progress_db.reset_data_base()
        time.sleep(60)
        t = str_time_t()


def change_time_null(string):
    string = string.split('\n')[1:]
    iphone_db.change_time(string)
    

def open_read_me():
    text = """Інструкція для самих маленьких!
Перед тобою мій юний друже дивний світ ремесла під назвою WorkProgress.
Тут ти будеш записувати свої досягнення, получати плюшки і бути красаучеком)
Зараз я тобі поясню як це все треба записувати щоб Флеркен не матюкався і все вірно рахував.
Нагадаю, що дана можливість розроблена у Флеркені тільки для того щоб ніякий персонаж не забував свої дії і якщо ще трішки почекати то розробник цеї байди зможе навчити тебе попадати ложкою в рот з першого разу за допомогою цього ж Флеркена!
Отже що треба робити?!
На протязі дня ти береш із бота всякі запчастини. Вони десь собі записуються.
В кінці дня ти скидуєш свій Work Progress(далі WP бо їбав писати кожен раз).
Воно це все рахує і каже "що саме і скільки треба взяти з бота ТА\АБО дописати у WP.
Можна робити по нормальному і відразу писати те що треба у WP коли шось зробив чи видав.(Але я ж знаю що такий шлях не для справжніх самураїв!!)
1. Заходите в меню команд 
2. Нажимаєте 'Other'.
3. Там є кнопка 'WorkProgress'. (про інші кнопки пізніше поясню або поясню усно)
4. Жмякаєш на цю кнопку і тебе перекидає в рядок щоб шось друкувати вже з готовим шаблоном.
 Зараз роскажу як користуватись шаблоном.
 - записуєш ремонт чи то клієнтський чи наш у відповідній категорії
 - форма запису наступна - "id2325 iphone 8Plus - нижній шлейф, нова акб, переклейка(проклейка 2, клей акб 2)"
 - детальніше "id\№\#(без пробіла)2351515(якщо номеру нема пишеш будь шо)(пробіл)iphone(пробіл)8Plus(конкретна модель без пробілів, велика чи мала буква різниці нема)-(дефіс, можна без пробілів по краях але краще з ними)"
 - детальніше друга половина "(тут був дефіс) шо зробив,(через кому наступне шо зробив)". Далі ти побачиш шо є якісь непонятні дужки. В них ти можеш писати все те саме що і до дужок але можна вказувати кількість, і також тут бажано писати проклейки і клей АКБ.
 - у дужках кількість пишеш через пробіл і потім через кому наступне.
 - ДО ДУЖОК кількість не пиши бо зламається))
 - якщо нема шо писати в дужках то їх можна не писати
 - ніяких номерів писати перед ремонтом не треба
 - кількість ремонтів по категоріях пишеш самостійно
 - щоб робити перенос в інший рядок треба нажимати CTRL + ENTER - це важливо!!!
 - коли все написав нажимаш ENTER і воно відправляється для порівняння і каже шо треба зробити. Все дуже просто, справишся навіть ти!
 - робити це все що воно просить ти можеш і потім, це не страшно.
5. Коли треба дописати ще шось у WP, робиш пункти 1, 2, 3! Відкривається вже збережена тобою робота що ти до цього писав. 
   Ніде записувати не треба, Флеркен буде памятати, а ти будеш собі просто дописувати.
6. В кінці дня чи там коли собі хочеш ти виконаєш то що просить бот, скидаєш ще раз той самий WP навіть не добавляючи нічого і він скаже чи все зійшлось.
7. Якщо все зійшлось то тобі повідомить Флеркен і можна буде нажати на кнопочку "Відправити". Її треба тиснути тільки тоді коли йдеш додому.
На рахунок інших кнопок:
1. "Обнулити свої дані" - тут ти можеш скинути все що ти написав у WP. Коли виникне ситуація що ти написув якусь дурню, а вона точно виникне я тебе знаю, ти моде онулити свої дані і написати все ще раз.
2. "Ресет бази шлангів" - це ти зможеш натиснути але нічо не станеться, бо ти ще манюній, мусік пусік такий. Доступ до цієї команди є тільки у мене і у Вані. Але якщо цікаво то ця команда чистить всю базу даних взагалі!
Повна очистка бази даних буде відбуватись автоматично кожен день зранку о "08:45"
3. "Зміна часу відсутніх позицій" - це якщо треба поміняти час коли скидується те чого нема. Короче не мав куди засунути цю функцію. Її не клацай.
"""
    return text

# print(open_read_me())

