import sqlite3
import sys
import csv

db = sqlite3.connect('chatbot.db')

cur = db.cursor()
rd=csv.reader(open('/Users/supriya/Applications/keywords.csv','r'),delimiter=',')
for row in rd:
        to_db=[unicode(row[0], "utf8"), unicode(row[1], "utf8"),unicode(row[2], "utf8"),unicode(row[3], "utf8")]
        st="INSERT INTO data (keywords, clmn, tbl, source) VALUES(?,?,?,?);"
        cur.execute(st,to_db)

db.commit()
db.close()

