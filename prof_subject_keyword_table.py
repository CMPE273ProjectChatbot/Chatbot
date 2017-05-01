import sqlite3

db = sqlite3.connect('chatbot.db')

cur = db.cursor()
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("who is taking", "instructor","course_info", "course")')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("who takes", "instructor","course_info", "course")')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("who is the faculty for", "instructor","course_info", "course")')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("who is the professor for", "instructor","course_info", "course")')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("who is teaching", "instructor","course_info", "course")')
cur.execute('INSERT INTO data (keywords, clmn, tbl, source) VALUES ("professor for", "instructor","course_info", "course")')
db.commit()
db.close()




