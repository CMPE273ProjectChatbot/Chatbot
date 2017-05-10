#!/usr/bin/python

import sqlite3
import sys
import csv

def create_connection():
    try:
        conn = sqlite3.connect('chatbot.db')
        return conn
    except Error as e:
        print(e)
 
    return None

#table creation
def create_table(conn):
	try:
        	c = conn.cursor()
       		c.execute('CREATE TABLE IF NOT EXISTS course_info(id REAL, course TEXT, course_name TEXT, section REAL, class_code TEXT, units REAL, class_format TEXT, class_type TEXT, seats TEXT, class_day TEXT, class_time TEXT, session TEXT, location TEXT, instructor TEXT)')

            	c.execute('CREATE TABLE IF NOT EXISTS lecture_type(code TEXT, description TEXT)')
            
            	c.execute('CREATE TABLE IF NOT EXISTS lecture_day(code TEXT, description TEXT)')
            
            	c.execute('CREATE TABLE IF NOT EXISTS course(code TEXT, name TEXT, description TEXT)')

		return c    		
	except Error as e:
        	print(e)


#course info data insertion
def data_entry_course_info(conn,c):
	rd=csv.reader(open('/Users/shirodkarrakesh/Downloads/course_info.csv','r'),delimiter=',')
    	for row in rd:
        	to_db=[unicode(row[0], "utf8"), unicode(row[1], "utf8"),unicode(row[2], "utf8"), unicode(row[3], "utf8"),unicode(row[4], "utf8"), unicode(row[5], "utf8"),unicode(row[6], "utf8"), unicode(row[7], "utf8"),unicode(row[8], "utf8"), unicode(row[9], "utf8"),unicode(row[10], "utf8"), unicode(row[11], "utf8"),unicode(row[12], "utf8"), unicode(row[13], "utf8"),]
        	st="INSERT INTO course_info (id,course,course_name,section,class_code,units,class_format,class_type,seats,class_day,class_time,session,location,instructor) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        	c.execute(st,to_db)

    	conn.commit()

#
def data_entry_lecture_type(conn,c):
    rd=csv.reader(open('/Users/shirodkarrakesh/Downloads/lecture_type.csv','r'),delimiter=',')
    for row in rd:
            to_db=[unicode(row[0], "utf8"), unicode(row[1], "utf8")]
            st="INSERT INTO lecture_type (code,description) VALUES(?,?);"
            c.execute(st,to_db)

    conn.commit()



def data_entry_lecture_day(conn,c):
    rd=csv.reader(open('/Users/shirodkarrakesh/Downloads/lecture_day.csv','r'),delimiter=',')
    for row in rd:
            to_db=[unicode(row[0], "utf8"), unicode(row[1], "utf8")]
            st="INSERT INTO lecture_day (code,description) VALUES(?,?);"
            c.execute(st,to_db)

    conn.commit()

def data_entry_course(conn,c):
    try:
        rd=csv.reader(open('/Users/shirodkarrakesh/Downloads/CMPEDescription.csv','r'),delimiter=',')
        for row in rd:
                to_db=[unicode(row[0], "utf8"), unicode(row[1], "utf8"),unicode(row[2], "utf8")]
                st="INSERT INTO course (code,name,description) VALUES(?,?,?);"
                c.execute(st,to_db)

        conn.commit()

    except Error as e:
        print(e)

def main():
	conn=create_connection()
	c=create_table(conn)
	data_entry_course_info(conn,c)
    	data_entry_lecture_type(conn,c)
    	data_entry_lecture_day(conn,c)
    	data_entry_course(conn,c)
    	c.close()
    	conn.close()

if __name__ =='__main__':
	main()
