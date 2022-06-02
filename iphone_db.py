import sqlite3
import os

with sqlite3. connect(os.path.join(os.path.dirname(__file__), 'iphone_parts.db'), check_same_thread=False) as db:

    cb = db.cursor()

#Запит на першому кроці
    def choise_models(search):
        result = cb.execute('SELECT model FROM models WHERE akb = ? OR glass = ? OR backlight = ? OR touch = ? OR frame = ? OR cover = ?', (search, search, search, search, search, search)).fetchall()
        return [i[0] for i in result]
        
# model = 'X'
    def choise_submodels(search, model):
        result = cb.execute(f'SELECT model FROM submodels WHERE akb = ? OR glass = ? OR backlight = ? OR touch = ? OR frame = ? OR cover = ?', (search, search, search, search, search, search,)).fetchall()
        return [i[0] for i in result if i[0][0] == model or i[0][:2] == model]
# model = 'XsMax'

    def choise_colors(search, model):
        return cb.execute(f'SELECT {search} FROM colors WHERE model = ?', (model,)).fetchall()[0][0]
        
s = ''
r = choise_colors('cover', '8Plus')
print(r)
if not r[0][0]:
    s += 'nocolor'
print(s)