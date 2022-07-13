import sqlite3
import os

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


    def all_sheets():
        return cb.execute('SELECT uk, round FROM keyboard').fetchall()


    def change_time(time, db = db):
        cb.execute(f'UPDATE time SET time = "{time}" WHERE count = 1')
        db.commit()
    

    def time_base():
        result = cb.execute('SELECT time FROM time WHERE count = 1').fetchall()[0]
        return result[0].split("'")[1]


    def maket():
        st = [
            'Переклеїв екранів -',
            'Видано готових - ',
            'Вдано клієнтських -',
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


    def select_work_progress(user):
        try:
            result = cb.execute(f"SELECT string_wp FROM {user}").fetchone()[0]
            return result
        except TypeError:
            return maket()
        except sqlite3.OperationalError:
            return maket()


    def select_glass_count(user):
        try:
            result = cb.execute(f"SELECT string_wp FROM {user} WHERE id = 2").fetchone()[0]
            return result
        except TypeError:
            return None
        # except sqlite3.OperationalError:
        #     return 0


    def update_work_progress(user, work_progress, st=True, db = db):
        work_progress = '\n'.join(work_progress.split('\n')[1:])
        cb.execute(f'UPDATE {user} SET string_wp = "{work_progress}" WHERE id = 1')
        if st:
            cb.execute(f'UPDATE {user} SET wp_number = 0')
            cb.execute(f'UPDATE {user} SET glass_count_wp = 0 WHERE id = 1')
        db.commit()


    def create_hose_table(user, db = db):
        cb.execute(f"""CREATE TABLE IF NOT EXISTS {user} (
                id INTEGER,
                device TEXT,
                number INTEGER,
                wp_device TEXT,
                wp_number INTEGER,
                string_wp TEXT,
                glass_count	INTEGER,
                glass_count_wp	INTEGER,
                PRIMARY KEY("id")
            )""")

        db.commit()


    def tabble_for_hose(user, args, db = db):
        create_hose_table(user)

        result = f'{args[0]} {args[1]} {args[2]}'

        glass_count = 0
        
        if args[2] == 'Скло':
            glass_count = int(args[-1])

        if not select_work_progress(user):
            cb.execute(f'INSERT INTO {user} (device, number, wp_device, wp_number, string_wp, glass_count, glass_count_wp) VALUES ("{result}", {int(args[-1])}, "{result}", 0, "{maket()}", {glass_count}, 0)')

        if cb.execute(f'SELECT device FROM {user} WHERE device = "{result}"').fetchone():
            cb.execute(f'UPDATE {user} SET number = number + {int(args[-1])} WHERE device = "{result}"')
            cb.execute(f'UPDATE {user} SET glass_count = glass_count + {glass_count} WHERE id = 1')
        else:
            cb.execute(f"INSERT INTO {user} (device, number, wp_device, wp_number) VALUES ('{result}', {int(args[-1])}, '{result}', 0)")
            cb.execute(f'UPDATE {user} SET glass_count = glass_count + {glass_count} WHERE id = 1')

        
        db.commit()


    def write_glass_count(user, number = 1, db = db):
        cb.execute(f"UPDATE {user} SET glass_count_wp = glass_count_wp + {number} WHERE id = 1")
        db.commit()


    def select_glass_count(user):
        result = cb.execute(f'SELECT glass_count, glass_count_wp FROM {user}').fetchone()
        result = list(map(lambda x: int(x), result))
        return result


    def delete_from_table(user, db = db):
        cb.execute(f"DELETE FROM {user}")
        db.commit()


    def select_table_user(user):
        try:
            return cb.execute(f"SELECT device, number, wp_number FROM {user}").fetchall()
        except sqlite3.OperationalError:
            return None
        
    
    def select_desc(parts):
        result = cb.execute(f'SELECT category, description FROM desc WHERE description LIKE "%{parts}%"').fetchall()
        if result:
            if parts in result[0][1].split('\r\n'):
                return result[0][0]
        else:
            return None


    def write_db_work_progress(user, string, number = 1, db = db):
        try:
            if cb.execute(f'SELECT wp_device FROM {user} WHERE wp_device = "{string}"').fetchone():
                cb.execute(f'UPDATE {user} SET wp_number = wp_number + {number} WHERE wp_device = "{string}"')
            else:
                if cb.execute(f'SELECT device FROM {user} WHERE device = "{string}"').fetchone():
                    cb.execute(f'UPDATE {user} SET wp_number = wp_number + {number} WHERE device = "{string}"')
                else:
                    cb.execute(f"INSERT INTO {user} (wp_device, wp_number, device, number) VALUES ('{string}', {number}, '{string}', 0)")
        except sqlite3.OperationalError:
            create_hose_table(user)
            write_db_work_progress(user, string)

        db.commit()


    
# tabble_for_hose('Ha3aVr', ['iphone', '5', 'Скло', 1])
# print(select_work_progress('Ha3aVr'))
# print(select_glass_count('Ha3aVr'))
# x = select_table_user('Ha3aVr')
# x = sorted(x, key=lambda x: 'Скло' not in x[0])
# print(x)