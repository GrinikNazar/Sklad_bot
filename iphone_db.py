import sqlite3
import os

with sqlite3. connect(os.path.join(os.path.dirname(__file__), 'iphone_parts.db'), check_same_thread=False) as db:

    cb = db.cursor()

#Запит на першому кроці
    def choise_models(search):
        result = cb.execute('SELECT model FROM models WHERE akb = ? OR glass = ? OR backlight = ? OR touch = ? OR frame = ? OR cover = ?', (search, search, search, search, search, search)).fetchall()
        return [i[0] for i in result]
        
# model = 'X'

# r = cb.execute(f'SELECT model FROM submodels WHERE akb = ? OR glass = ? OR backlight = ? OR touch = ? OR frame = ? OR cover = ? AND model LIKE "{model}%"', (search, search, search, search, search, search,)).fetchall()
# print(r)
# for i in r:
#     print(i[0])

# model = 'XsMax'

# r = cb.execute(f'SELECT {search} FROM colors WHERE model = ?', (model,)).fetchall()
# print(r[0][0])