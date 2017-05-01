import sqlite3
import sys
import csv

db = sqlite3.connect('chatbot.db')
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS data (keywords, clmn, tbl, source);")
filename = '/Users/vimalraj/Documents/CMPE273Project/keywords.csv'
filename.encode('utf-8')
with open(filename, 'rb') as data:
    csvDict = csv.DictReader(data)
    to_db = []
    for i in csvDict:
        to_db.append((i['keywords'], i['clmn'], i['tbl'], i['source']))
    print "to_db", to_db
cur.executemany("INSERT INTO data (keywords, clmn, tbl, source) VALUES (?, ?, ?, ?);", to_db)

db.commit()
db.close()
