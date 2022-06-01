import sqlite3
import os

db = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'iphone_parts.db'))

c = db.cursor()

cover = 'cover'
model = 'model'

r = c.execute('SELECT model FROM models WHERE (?) = 1', (cover,)).fetchall()

print(r)

db.close()