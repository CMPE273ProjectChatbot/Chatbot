import sqlite3

db = sqlite3.connect('chatbot.db')

cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS greet(req TEXT, res TEXT)')
cur.execute('INSERT INTO greet (req, res) VALUES ("hi", "Hello There!!")')
cur.execute('INSERT INTO greet (req, res) VALUES ("hello", "Hi! How can I help you?")')
cur.execute('INSERT INTO greet (req, res) VALUES ("have a wonderful day", "Thank you! you too!")')
cur.execute('INSERT INTO greet (req, res) VALUES ("bye", "Bye! Have a good day")')
cur.execute('INSERT INTO greet (req, res) VALUES ("have a good day", "Thank you! you too!")')
cur.execute('INSERT INTO greet (req, res) VALUES ("cya", "Bye!")')
cur.execute('INSERT INTO greet (req, res) VALUES ("have a nice day", "Thank you! you too!")')
cur.execute('INSERT INTO greet (req, res) VALUES ("thank you", "You are welcome.")')
cur.execute('INSERT INTO greet (req, res) VALUES ("thank you bye", "welcome bye.")')
db.commit()
db.close()




