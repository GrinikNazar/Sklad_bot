import datetime
import conf
import random
import gspread


# визначення попередньої дати
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


def search_coordinate(wks):
    col_val_coord = wks.col_values(2)
    col_val_coord = list(set(col_val_coord))
    col_val_coord = [x for x in col_val_coord if x != ''] # Знаходить координати кожного користувача

    return col_val_coord


def get_path_and_worksheet():
    sh = conf.source_google_sheet_api(conf.work_progress_table)
    wks = sh.worksheet('Example')

    return {'wks': wks, 'sh': sh}
          

def get_user_score_when_came_to_point(user_id):
    wks = get_path_and_worksheet()['wks']
    sh = conf.source_google_sheet_api(conf.work_progress_table)
    user_id = str(user_id)
    now_data = datetime.datetime.date(datetime.datetime.now())
    data_string = datetime.datetime.strftime(now_data, '%m-%Y')
    try:
        wks = sh.worksheet(data_string)
    except gspread.exceptions.WorksheetNotFound:
        wks.duplicate(new_sheet_name=data_string)
        wks = sh.worksheet(data_string)
    col_val_id = wks.col_values(1)
    for i, row in enumerate(col_val_id):
        if row == user_id:
            row_values = wks.row_values(i + 1)
            break
    user_coord = row_values[1]
    user_coord = user_coord.replace('8', '2')

    return wks.acell(user_coord).value


def get_variant_string(user_name, label):
    dict_of_variant_label = {
        100: (
            f'🥉🥉🥉{user_name}🥉🥉🥉\nНе дарма ходив на роботу і вже дійшов до позначки у 1️⃣0️⃣0️⃣ балів!\n👍👍!так тримати!👍👍',
            f'🥉🥉🥉{user_name}🥉🥉🥉\nНаробився цих мобілок на1️⃣0️⃣0️⃣ балів!\n👍👍Не збавляй темп👍👍',
            f'🥉🥉🥉{user_name}🥉🥉🥉\nМолодець, но поки набрав тільки 1️⃣0️⃣0️⃣ балів!\n👍👍Вали шо КІНЬ👍👍',
            f'🥉🥉🥉{user_name}🥉🥉🥉\nДійшов до 1️⃣0️⃣0️⃣.\nВже не просто пятюню отримаєш в кінці)\n👍👍Не здаватись, тільки вперед, тільки більше👍👍'
        ),
        120: (
            f'🥈🥈🥈{user_name}🥈🥈🥈\nФлеркен каже що вже маєш 1️⃣2️⃣0️⃣ балів!\n👍👍Супер давай ще👍👍',
            f'🥈🥈🥈{user_name}🥈🥈🥈\nВже 1️⃣2️⃣0️⃣ балів є, якщо набереш ще 20 то разом буде 140🤔!\n👍👍 !так тримати!👍👍',
            f'🥈🥈🥈{user_name}🥈🥈🥈\nПоки 1️⃣2️⃣0️⃣ але це ж тільки початок, так?\n👍👍 Так?👍👍'
        ),
        140: (
            f'🥇🥇🥇{user_name}🥇🥇🥇\nТак так так  1️⃣4️⃣0️⃣\nок, ще почекаємо...\n👍👍Хороша робота!👍👍',
            f'🥇🥇🥇{user_name}🥇🥇🥇\nВоу воу воу, розігнався вже до  1️⃣4️⃣0️⃣, супер!\n👍👍Не збавляй темп👍👍',
            f'🥇🥇🥇{user_name}🥇🥇🥇\nТак так так, вже схоже на результат\n1️⃣4️⃣0️⃣ набрав і непомітив.\n👍👍 Далі буде...👍👍',
        ),
        160: (
            f'🏅🏅🏅{user_name}🏅🏅🏅\nХороший результат в  1️⃣6️⃣0️⃣ за місяць\n👍👍 Ти на вірному шляху не зупиняйся👍👍',
            f'🏅🏅🏅{user_name}🏅🏅🏅\nGood job 1️⃣6️⃣0️⃣ to be continued....\n👍👍 Congratulation!👍👍',
            f'🏅🏅🏅{user_name}🏅🏅🏅\nФайно вийшло - 1️⃣6️⃣0️⃣ взяв.\nЩе трохи і буде 160 + трохи)))\n👍👍 продовжуй в цьому ж дусі👍👍',
        ),
        180: (
            f'🏆🏆🏆{user_name}🏆🏆🏆\nМої вітання 1️⃣8️⃣0️⃣ балів за місяць це гідно\n👍👍Сильно👍👍',
            f'🏆🏆🏆{user_name}🏆🏆🏆\nЧудовий результат в 1️⃣8️⃣0️⃣ балів.\n👍👍Молодцом👍👍',
            f'🏆🏆🏆{user_name}🏆🏆🏆\nНе всі можуть набрати 1️⃣8️⃣0️⃣ балів.\nВірніше не тільки лиш всі можуть набрати 1️⃣8️⃣0️⃣ балів.\nМало хто може це зробити\n👍👍  📎 👍👍'
        ),
        200: (
            f'👑👑👑{user_name}👑👑👑\nMVP OF MONTHS\n 2️⃣0️⃣0️⃣\n👍👍 Можна йти додому 👍👍',
            f'👑👑👑{user_name}👑👑👑\nКращий з кращих\n 2️⃣0️⃣0️⃣\n👍👍  Можна й по хвастастись 👍👍'
        )
    }

    return random.choice(dict_of_variant_label[label])


def compare_scores(user_name, begin_value: str, end_value: str) -> str:
    begin_value = float(begin_value.replace(',', '.'))
    end_value = float(end_value.replace(',', '.'))
    table_score_label = (100, 120, 140, 160, 180, 200)
    for label in table_score_label:
        if begin_value < label and end_value >= label:
            return get_variant_string(user_name, label)


def get_now_day() -> int: 
    now_data = datetime.datetime.date(datetime.datetime.now())
    now_data_int = int(datetime.datetime.strftime(now_data, '%d')) #цей день 

    return now_data_int


def total_scores():
    sh = conf.source_google_sheet_api(conf.work_progress_table)
    pre_date = previos_date()
    wks = sh.worksheet(pre_date) # конект до таблиці попереднього місяця
    coordinate = search_coordinate(wks) # [D8:E8, F8:G8, H8:I8, J8:K8, L8:M8]

    score_money = {
        (100, 120): 300,
        (120, 140): 500,
        (140, 160): 700,
        (160, 180): 1000,
        (180, 200): 1500,
        (200, 1000): 2000
        }

    name_user = '1'
    total_scores = '2'
    score_dict = {}
    best_day_dict = {}
    sum_scores = {}

    for result in coordinate:
        result_coord = result.replace('8', total_scores)
        res_total_scores = round(float(wks.acell(result_coord).value.replace(',', '.')), 2)
        
        user_name_coord = result.replace('8', name_user)
        user_name = wks.acell(user_name_coord).value

        best_d = int(wks.acell(result).value)

        best_day_dict[user_name] = best_d
        score_dict[user_name] = res_total_scores

        for key, value in score_money.items():
            if res_total_scores >= key[0] and res_total_scores < key[1]:
                sum_scores[user_name] = value + best_d * 30
                break
            else:
                if best_d == 0:
                    sum_scores[user_name] = '✋'
                else:
                    sum_scores[user_name] = best_d * 30
    
    result_string_of_scores = ''
    sorted_dict_to_list_keys= sorted(score_dict, key=score_dict.get, reverse=True) # повертає ключі посортованого словника по значеннях 
    for i, key in enumerate(sorted_dict_to_list_keys):
        number_user = i + 1
        sum_money_total = sum_scores[key]
        label_position = ''
        label_position_uah = 'грн'
        if number_user == 1:
            sum_money_total += 700
            label_position = '👑'
        elif number_user == 2:
            sum_money_total += 400
            label_position = '🏅'
        if sum_money_total == '✋':
            label_position_uah = ''

        result_string_of_scores += f'{number_user}.{label_position}{key} ({score_dict[key]}-балів) (Best D.- {best_day_dict[key]}) {sum_money_total}{label_position_uah}\n'

    return result_string_of_scores.rstrip()


def main(bot, chat): #Викликати 1 числа нового місяця о 10:00 на часовій мітці
    if get_now_day() == 1:
        bot.send_message(chat, total_scores())
