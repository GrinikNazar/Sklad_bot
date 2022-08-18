import sqlite3
import os
from fuzzywuzzy import fuzz
from iphone_db import compare_fuz
from handler_wp import wp_handler_text, string_separate
from work_progress_db import select_work_progress
from handler_wp import get_count_glass_replace

with sqlite3. connect(os.path.join(os.path.dirname(__file__), 'iphone_parts.db'), check_same_thread=False) as db:

    cb = db.cursor()


    def select_scores(model, user_job):
        list_for_compare = []
        list_for_compare_db = cb.execute(f'SELECT part FROM scores').fetchall()
        for string in list_for_compare_db:
            list_for_compare.extend(string[0].split('\r\n'))

        result_list = compare_fuz(list_for_compare, user_job, 85)

        if len(result_list) == 1:
            part = result_list[0]
            result = cb.execute(f'SELECT "{model}" FROM scores WHERE part LIKE "%{part}%"').fetchall()
            try:
                result = float(result[0][0])
            except TypeError:
                result = 0
            return result
        else:
            return None


    def main_scores():
        dict_id_user_job = {}
        final_maket = select_work_progress(375385945) #цей параметр має передаватись як аргумент. Запит до бази звідси видалити 
        result = wp_handler_text(final_maket, 'need_dict')
        glass_count = get_count_glass_replace(final_maket, from_massage='from_db')
        sum_glass_count = glass_count * 0.5 #сума балів за переклейки зверху
        
        sum_user_job = 0
        sum_instyle_job = 0
        sum_client_job = 0
        for key, value in result.items():
            for user_job in value:
                id_job = user_job.split(' ')[0]
                score = string_separate(user_job, select_scores)[0]
                if key == 'Клієнтські':
                    score += score * 0.2
                    score = round(score, 3)
                dict_id_user_job[id_job] = score
                sum_user_job += score
                if key == 'Клієнтські':
                    sum_client_job += score
                elif key == 'Готові':
                    sum_instyle_job += score

        split_maket = final_maket.split('\n')
        result_maket = []
        for string_split in split_maket:
            key_id = string_split.split(' ')[0]
            if key_id == 'Переклеїв' and sum_glass_count != 0:
                sum_user_job += sum_glass_count
                string_split += f' ({sum_glass_count})'
            elif 'Видано готових' in string_split:
                string_split += f' ({round(sum_instyle_job, 3)})'
            elif 'Видано клієнтських' in string_split:
                string_split += f' ({round(sum_client_job, 3)})'
            elif key_id in dict_id_user_job:
                string_split += f' ({dict_id_user_job[key_id]})'
            result_maket.append(string_split)
        result_maket.append('')
        result_maket.append(f'Загальний результат - {round(sum_user_job, 3)}')
        final_maket = '\n'.join(result_maket)
        return final_maket


# print(main_scores())