#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('chatbot.db')
print "Opened database successfully";

course='CMPE 030'
cursor = conn.execute("SELECT course_name from course_info where course=:id",{"id":course})
conn.commit()
row=cursor.fetchone()
print  row[0]

print "Operation done successfully";
conn.close()
