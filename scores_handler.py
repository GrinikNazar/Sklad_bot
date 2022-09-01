import sqlite3
import os
from fuzzywuzzy import fuzz
import bot
from iphone_db import compare_fuz
import handler_wp 
import work_progress_db 
import excel_score_handlen

with sqlite3. connect(os.path.join(os.path.dirname(__file__), 'iphone_parts.db'), check_same_thread=False) as db:

    cb = db.cursor()


    def select_scores(model, user_job):
        list_for_compare = []
        list_for_compare_db = cb.execute(f'SELECT jobs FROM from_excel_table_score').fetchall()
        for string in list_for_compare_db:
            list_for_compare.extend(string[0].split('\n'))

        result_list = compare_fuz(list_for_compare, user_job, 85)

        if len(result_list) == 1:
            part = result_list[0]
            result = cb.execute(f'SELECT "{model}" FROM from_excel_table_score WHERE jobs LIKE "%{part}%"').fetchall()
            try:
                result = float(result[0][0])
            except TypeError:
                result = 0
            except ValueError:
                result = 0
            return result
        else:
            return 0

    # '!2.3'
    def custom_scores_search(user_job: str, user_id):
        user_job_symbol = '!'
        user_job = user_job.split(user_job_symbol)
        if len(user_job) > 1:
            try:
                score = float(user_job[1])
            except ValueError:
                message = 'Свій варіант балів треба писати через точку "."'
                bot.bot_error_message(user_id, message)
                score = 0
        else:
            score = 0
        return score


    def delete_custom_scores(string_split: str) -> str:
        string_split = string_split.split('!')
        return string_split[0].rstrip()


    def main_scores(id_user = 375385945, *args):
        dict_id_user_job = {}
        final_maket = work_progress_db.select_work_progress(id_user)
        result = handler_wp.wp_handler_text(final_maket, 'need_dict')
        glass_count = handler_wp.get_count_glass_replace(final_maket, from_massage='from_db') #кількість переклейок зверху
        sum_glass_count = glass_count * 0.5 #сума балів за переклейки зверху
        
        sum_user_job = 0 #загальна сума балів
        sum_instyle_job = sum_glass_count #сума за наші
        sum_client_job = 0 #сума за клієнтські
        count_client = 0 #рахує кількість телефонів клієнтських
        count_instyle = 0 #кількість телефонів наших
        list_null_score = []

        #Підрахунок балів
        for key, value in result.items():
            for user_job in value:
                id_job = user_job.split(' ')[0]
                custom_score = custom_scores_search(user_job, id_user) #пошук символа з балами які поставив користувач
                if custom_score == 0:
                    score_tuple = handler_wp.string_separate(user_job, select_scores)
                    score = score_tuple[0][0]
                    for score_list in score_tuple[1]:
                        check_score = float(score_list.split(' ')[-1])
                        if check_score == 0.0:
                            list_null_score.append(f'{user_job} | {score_list}')
                else:
                    score = custom_score
                if key == 'Клієнтські':
                    score += score * 0.2
                    score = round(score, 3)
                dict_id_user_job[id_job] = score
                sum_user_job += score

                if key == 'Клієнтські': #загальні бали за клієнтські ремонти
                    sum_client_job += score
                    count_client += 1
                elif key == 'Готові': #бали за готові ремонти
                    sum_instyle_job += score
                    count_instyle += 1

        if args:
            return list_null_score

        #Запис в кінечну форму балів
        split_maket = final_maket.split('\n')
        result_maket = []
        for string_split in split_maket:
            key_id = string_split.split(' ')[0]
            string_split = delete_custom_scores(string_split)
            if key_id == 'Переклеїв' and sum_glass_count != 0:
                sum_user_job += sum_glass_count
                string_split += f' ({sum_glass_count})'
            elif 'Видано готових' in string_split:
                string_split += f' {count_instyle} ({round(sum_instyle_job, 2)})'
            elif 'Видано клієнтських' in string_split:
                string_split += f' {count_client} ({round(sum_client_job, 2)})'
            elif key_id in dict_id_user_job:
                string_split += f' ({dict_id_user_job[key_id]})'
            result_maket.append(string_split)
        result_maket.append('')
        result_maket.append(f'Загальний результат - {round(sum_user_job, 3)}')
        final_maket = '\n'.join(result_maket)

        score_tuple = (sum_instyle_job, sum_client_job, count_instyle, count_client, glass_count)
        excel_score_handlen.main_excel(id_user, score_tuple) #запис у excel таблицю

        return final_maket
