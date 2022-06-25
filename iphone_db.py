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


# print(choise_submodels('touch', 'mini'))
# print(gen_keyboard('АКБ'))
