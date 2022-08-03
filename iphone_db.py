import sqlite3
import os
import work_progress_db
from fuzzywuzzy import fuzz

with sqlite3. connect(os.path.join(os.path.dirname(__file__), 'iphone_parts.db'), check_same_thread=False) as db:

    cb = db.cursor()


#Запит на першому кроці
    def choise_models(search):
        result = cb.execute('SELECT model FROM models WHERE akb = ? OR glass = ? OR backlight = ? OR touch = ? OR frame = ? OR cover = ? OR copy = ? OR gluepr = ? OR other = ?', (search, search, search, search, search, search, search, search, search)).fetchall()
        return [i[0] for i in result]


    def artic(model):
        result = cb.execute('SELECT article FROM models WHERE model = ?',(model,)).fetchone()
        return result[0]
        
        
#Запит на другому кроці
    def choise_submodels(search, model):
        result = cb.execute(f'SELECT model, article FROM submodels WHERE akb = ? OR glass = ? OR backlight = ? OR touch = ? OR frame = ? OR cover = ? OR copy = ? OR gluepr = ? OR other = ?', (search, search, search, search, search, search, search, search, search,)).fetchall()
        return [i[0] for i in result if i[1] == model]


#Запит для вибору кольору
    def choise_colors(search, model):
        return cb.execute(f'SELECT {search} FROM colors WHERE model = ?', (model,)).fetchall()[0][0]


    def gen_keyboard(uk):
        return cb.execute('SELECT eng, list FROM keyboard WHERE uk = ?', (uk,)).fetchone()
    

    def ret_uk_request(en):
        return cb.execute('SELECT uk FROM keyboard WHERE eng = ?', (en,)).fetchone()[0]


    def get_smiles_from_db(en):
        return cb.execute('SELECT smiles FROM keyboard WHERE eng = ?', (en,)).fetchone()[0]


    def all_sheets():
        return cb.execute('SELECT uk, round FROM keyboard').fetchall()


    def change_time(time, db = db):
        cb.execute(f'UPDATE time SET time = "{time}" WHERE count = 1')
        db.commit()
    

    def time_base(string_time_value):
        count = 0
        if string_time_value == 'null_time':
            count = 1
        elif string_time_value == 'reset_time':
            count = 2
        elif string_time_value == 'wp_reminder':
            count = 3
        result = cb.execute(f'SELECT time FROM time WHERE count = {count}').fetchall()[0]
        return result[0].split("'")[1]


    def select_hose():
        result = cb.execute(f"SELECT name, telid FROM users").fetchall()
        return dict(result)


    #функція запису в базу коли жмуть конфірм 
    def write_confirm_user(user_id, db = db):
        cb.execute(f'UPDATE users SET confirm = confirm + 1 WHERE telid = {user_id}')
        db.commit()
    

    #функція яка витягує ід користувачів які не скинули WP
    def get_users_where_confirm_null():
        result = cb.execute("SELECT telid FROM users WHERE confirm = 0").fetchall()
        result = [x[0] for x in result]
        return result


    #обнулення даних confirm
    def make_null_confirm_data(db = db):
        cb.execute(f'UPDATE users SET confirm = 0')
        cb.execute(f"UPDATE users SET confirm = 1 WHERE name = 'Ваня'")
        db.commit()


    def reset_to_null_user_from_button(user_id, db = db):
        cb.execute(f'UPDATE users SET confirm = 0 WHERE telid = {user_id}')
        db.commit()


    #функція для неявного порівняння
    def compare_fuz(list_for_compare, part, variation):
        result_list = []
        number_compare = variation
        while number_compare != 100:
            for i in list_for_compare:
                if fuzz.ratio(i.lower(), part.lower()) > number_compare:
                    result_list.append(i)
            if len(result_list) == 1:
                break
            else:
                number_compare += 5
                result_list = []
        return result_list
  
    
    def select_desc(parts):
        list_for_compare = []
        list_for_compare_db = cb.execute(f'SELECT description FROM desc').fetchall()
        for string in list_for_compare_db:
            list_for_compare.extend(string[0].split('\r\n'))

        result_list = compare_fuz(list_for_compare, parts, 80)

        if len(result_list) == 1:
            part = result_list[0]
            result = cb.execute(f'SELECT category, description FROM desc WHERE description LIKE "%{part}%"').fetchall()
            if result:
                if part in result[0][1].split('\r\n'):
                    return result[0][0]
        else:
            return None

    
    #для визначення дозволу
    def select_telephone_models_where_yes():
        result = cb.execute(f"SELECT name FROM telephone_models WHERE permission = 'yes'").fetchall()
        result = [x[0] for x in result]
        return result

    
    #використати для не явного порівняння
    def select_all_telephone_name(model):
        result = cb.execute(f"SELECT name FROM telephone_models").fetchall()
        result = [x[0] for x in result]

        result_list = compare_fuz(result, model, 60)

        return result_list[0]


    #Добавити в базу користувача
    def write_new_user_to_data_base(user_name, user_id, db = db):
        select_request = cb.execute(f"SELECT name, telid FROM users WHERE telid = {user_id}").fetchone()
        if select_request is None or select_request[-1] != user_id:
            cb.execute(f"INSERT INTO users (name, telid, confirm) VALUES ('{user_name}', {user_id}, 0)")
            db.commit()
            work_progress_db.create_table_users(user_id)
            work_progress_db.create_table_glass(user_id)
            work_progress_db.create_table_users_maket(user_id)
        elif select_request[-1] == user_id:
            return 'Такий користувач вже зареєстрований!'
            
        return 'Користувача добавлено!'


    def delete_from_db_users(user_id, db = db):
        cb.execute(f"DELETE FROM users WHERE telid = {user_id}")
        db.commit()
        work_progress_db.drop_table_user(user_id)


# write_new_user_to_data_base('bodnariukkk', 603519506)
