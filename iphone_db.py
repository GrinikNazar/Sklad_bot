import sqlite3
import os

db = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'iphone_parts.db'))

cb = db.cursor()

search = 'cover'

# r = cb.execute('SELECT model FROM models WHERE akb = ? OR glass = ? OR backlight = ? OR touch = ? OR frame = ? OR cover = ?', (search, search, search, search, search, search)).fetchall()
# print(r)

model = '8'

r = cb.execute('SELECT cover FROM colors WHERE model = ?', (model,)).fetchall()
print(r[0][0])

print(r[0][0].split('\r\n'))
db.close()