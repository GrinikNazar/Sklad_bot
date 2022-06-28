import engine
import iphone_db


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
            sum_strings += len(v)

    s_a = round(sum_strings / len(list_of_values))
    sa_string = ''
    for i in range(s_a):
        sa_string += '-'

    work_progress = iphone_db.select_table_user('Ha3aVr')
    
    result_string = ''
    if len(list_of_values) >= len(work_progress):
        for row in range(len(list_of_values)):
            if work_progress[row][0] not in locals():
                result_string += f'{row + 1}. {list_of_values[row]} {sa_string} '
            else:
                result_string += f'{row + 1}. {list_of_values[row]} {sa_string} {work_progress[row][0]}\n'


    return result_string


# print(handler_wp(engine.maket()))