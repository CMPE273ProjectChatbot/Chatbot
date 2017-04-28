import sqlite3

db = sqlite3.connect('chatbot.db')

cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS data(keywords TEXT, clmn TEXT, tbl TEXT, source TEXT)')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("What is", "name,description","course", "code")')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("description", "name,description","course", "code")')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("name course", "name","course", "code")')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("course", "name,description","course", "code")')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("code", "code","course", "name")')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("describe course", "name,description","course", "code")')

db.commit()
db.close()




