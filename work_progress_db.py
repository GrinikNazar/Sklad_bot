import sqlite3
import os

users = {
    'Назар': 375385945,
    'Ваня': 239724045,
    'Саша': 350257882,
    'Артур': 372369919,
    'Льоша': 522646080,
    'Вадим': 1318753542
}

with sqlite3.connect(os.path.join(os.path.dirname(__file__), 'work_progress.db'), check_same_thread=False) as db:

    cb = db.cursor()

    def create_table_users(user_id, db = db):
        cb.execute(f"""CREATE TABLE IF NOT EXISTS '{user_id}' (
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


    def delete_from_table(user_id, db = db):
        cb.execute(f"DELETE FROM '{user_id}'")
        cb.execute(f"DELETE FROM '{user_id}_maket'")
        db.commit()


    def select_work_progress(user):
        try:
            result = cb.execute(f"SELECT string_wp FROM {user}").fetchone()[0]
            return result
        except TypeError:
            return maket()
        except sqlite3.OperationalError:
            return maket()

    
    def tabble_for_hose(user, args, db = db):

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

        

for user in users.values():
    create_table_users(user)
    create_table_users_maket(user)