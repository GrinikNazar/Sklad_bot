import sqlite3
import os
import iphone_db

with sqlite3.connect(os.path.join(os.path.dirname(__file__), 'work_progress.db'), check_same_thread=False) as db:

    cb = db.cursor()

    def create_table_users(user_id, db = db):
        cb.execute(f"""CREATE TABLE IF NOT EXISTS '{user_id}' (
                id INTEGER,
                device TEXT,
                number INTEGER,
                wp_number INTEGER,
                PRIMARY KEY("id")
                )""")

        db.commit()


    #Функція для створення таблиці з макетом
    def create_table_users_maket(user_id, db = db):
        cb.execute(f"""CREATE TABLE IF NOT EXISTS '{user_id}_maket' (
                id INTEGER,
                wp TEXT,
                PRIMARY KEY("id")
                )""")

        sel_maket = cb.execute(f"SELECT wp FROM '{user_id}_maket'").fetchone()
        
        if not sel_maket:
            cb.execute(f"INSERT INTO '{user_id}_maket' (wp) VALUES ('{maket()}')")
        else:
            cb.execute(f"UPDATE '{user_id}_maket' SET wp = '{maket()}' WHERE id = 1")

        db.commit()


    def create_table_glass(user_id, db = db):
        cb.execute(f"""CREATE TABLE IF NOT EXISTS '{user_id}_glass' (
                id INTEGER,
                device TEXT,
                glass_from_bot INTEGER,
                glass_wp INTEGER,
                PRIMARY KEY("id")
                )""")

        db.commit()


    def maket():
        st = [
            'Переклеїв екранів - ',
            'Видано готових - ',
            'Вдано клієнтських - ',
            'Не виданих - ',
            '',
            'Готові',
            '',
            '',
            'Клієнтські',
            '',
            '',
        ]
        return '\n'.join(st)

    
    #Вибрати всі дані для порівняння
    def select_table_user(user):
        # try:
        return cb.execute(f"SELECT device, number, wp_number FROM '{user}'").fetchall()
        # except sqlite3.OperationalError:
        #     return None

    
    def select_table_user_glass(user):
        return cb.execute(f"SELECT device, glass_from_bot, glass_wp FROM '{user}_glass'").fetchall()

    
    def delete_from_table(user_id, db = db):
        cb.execute(f"DELETE FROM '{user_id}'")
        cb.execute(f"DELETE FROM '{user_id}_maket'")
        cb.execute(f"DELETE FROM '{user_id}_glass'")
        db.commit()

    
    #обнулити дані з work_progress
    def delete_user_work_progress(user_id, db = db):
        cb.execute(f"UPDATE '{user_id}' SET wp_number = 0")
        cb.execute(f"UPDATE '{user_id}_glass' SET glass_wp = 0")
        cb.execute(f"DELETE FROM '{user_id}_maket'")
        create_table_users_maket(user_id)

        db.commit()


    #витягнути дані з макет останні або макет
    def select_work_progress(user):
        # try:
        result = cb.execute(f"SELECT wp FROM '{user}_maket'").fetchall()
        return result[-1][0]
        # except TypeError:
        #     return maket()
        # except sqlite3.OperationalError:
        #     return maket()

    
    #Збереження значень кожної запчастини коли беруть з бота
    def tabble_for_hose(user, args, db = db):

        result = f'{args[0]} {args[1]} {args[2]}'

        glass_count = 0
        
        if args[2] == 'Скло':
            glass_count = int(args[-1])
            #записувати в таблицю з склом
            if cb.execute(f'SELECT device FROM "{user}_glass" WHERE device = "{result}"').fetchone():
                if cb.execute(f"SELECT glass_from_bot FROM '{user}_glass' WHERE device = '{result}'").fetchone()[0]:
                    cb.execute(f'UPDATE "{user}_glass" SET glass_from_bot = glass_from_bot + {glass_count} WHERE device = "{result}"')
                else:
                    cb.execute(f'UPDATE "{user}_glass" SET glass_from_bot = {glass_count} WHERE device = "{result}"')
            else:
                cb.execute(f"INSERT INTO '{user}_glass' (device, glass_from_bot, glass_wp) VALUES ('{result}', {glass_count}, 0)")
        else:
            if cb.execute(f'SELECT device FROM "{user}" WHERE device = "{result}"').fetchone(): 
                cb.execute(f'UPDATE "{user}" SET number = number + {int(args[-1])} WHERE device = "{result}"')   
            else:
                cb.execute(f"INSERT INTO '{user}' (device, number, wp_number) VALUES ('{result}', {int(args[-1])}, 0)")

        db.commit()


    #Зберігати у id_maket кожен раз новий запис
    def update_work_progress(user, work_progress, st=True, db = db):
        work_progress = '\n'.join(work_progress.split('\n')[1:])
        if select_work_progress(user) != work_progress:
            cb.execute(f"INSERT INTO '{user}_maket' (wp) VALUES ('{work_progress}')")

        db.commit()


    #Зберегти в таблиці запчастини які скидують в рогрес
    def write_db_work_progress(user, string, number = 1, db = db):

        #записати в таблицю з склом
        #заборонити добавляти скло у загальну табличку
        glass = 'Скло'
        #для скла своя таблиця
        if glass in string:
            if cb.execute(f'SELECT device FROM "{user}_glass" WHERE device = "{string}"').fetchone():
                if cb.execute(f"SELECT glass_wp FROM '{user}_glass' WHERE device = '{string}'").fetchone()[0]:
                    cb.execute(f'UPDATE "{user}_glass" SET glass_wp = glass_wp + {number} WHERE device = "{string}"')
                else:
                    cb.execute(f'UPDATE "{user}_glass" SET glass_wp = {number} WHERE device = "{string}"')
            else:
                cb.execute(f"INSERT INTO '{user}_glass' (device, glass_wp, glass_from_bot) VALUES ('{string}', {number}, 0)")
        #все інше
        else:
            if cb.execute(f'SELECT device FROM "{user}" WHERE device = "{string}"').fetchone():
                cb.execute(f'UPDATE "{user}" SET wp_number = wp_number + {number} WHERE device = "{string}"')
            else:
                if cb.execute(f'SELECT device FROM "{user}" WHERE device = "{string}"').fetchone():
                    cb.execute(f'UPDATE "{user}" SET wp_number = wp_number + {number} WHERE device = "{string}"')
                else:
                    cb.execute(f'INSERT INTO "{user}" (wp_number, device, number) VALUES ({number}, "{string}", 0)')

        db.commit()


    def reset_data_base():
        users = iphone_db.select_hose()
        for user in users.values():
            delete_from_table(user)
            create_table_users(user)
            create_table_users_maket(user)
            create_table_glass(user)


# reset_data_base()
# print(select_work_progress(375385945))