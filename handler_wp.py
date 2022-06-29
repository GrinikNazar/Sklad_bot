import engine
import iphone_db

def sa_string(string):
        mb_string = 20
        pro_string = 20
        result_string = ['', '']
        result = mb_string - len(string)
        result_2 = pro_string - len(string)
        for i in range(result):
            result_string[0] += '-'
        for i in range(result_2):
            result_string[1] += ' '
        return result_string


def handler_wp(message):
    marker = ''
    d = {
        'Готові': [],
        'Клієнтські': [],
        'Не видані': []
    }

    message = message[message.index('Готові'):]

    for msg in message.split('\n'):  
        if msg in d.keys():
            marker = msg
        elif not msg:
            continue
        else:
            d[marker].append(msg)

    # list_of_values = [v for value in d.values() for v in value]
    list_of_values = []

    sum_strings = 0
    for value in d.values():
        for v in value:
            list_of_values.append(v)

    work_progress = iphone_db.select_table_user('Ha3aVr')

    
    result_string = ''
    if len(list_of_values) >= len(work_progress):
        for row in range(len(list_of_values)):
            if row > len(work_progress) - 1:
                result_string += f'{row + 1}. {list_of_values[row]} {sa_string} {row + 1}. " "'
            else:
                result_string += f'{row + 1}. {list_of_values[row]} {sa_string} {row + 1}. {work_progress[row][0]}\n'

    else:
        for row in range(len(work_progress)):
            if row > len(list_of_values) - 1:
                result_string += f'{row + 1}. " " {sa_string("   ")} {row + 1}. {work_progress[row][0]}\n'
            else:
                result_string += f'{row + 1}. {work_progress[row][0] + sa_string(work_progress[row][0])[1]} {sa_string(work_progress[row][0])[0]} {row + 1}. {list_of_values[row]}\n'


    return result_string.rstrip()


# print(handler_wp(engine.maket()))