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

            	c.execute('CREATE TABLE IF NOT EXISTS prof_office_hour(prof_name TEXT, time TEXT)')

		return c    		
	except Error as e:
        	print(e)



def data_entry_hour(conn,c):
        rd=csv.reader(open('/Users/shirodkarrakesh/Downloads/prof_office_hour.csv','r'),delimiter=',')
        for row in rd:
                to_db=[unicode(row[0], "utf8"), unicode(row[1], "utf8")]
                st="INSERT INTO prof_office_hour (prof_name,time) VALUES(?,?);"
                c.execute(st,to_db)

        conn.commit()


def main():
	conn=create_connection()
	c=create_table(conn)
	data_entry_hour(conn,c)
    	c.close()
    	conn.close()

if __name__ =='__main__':
	main()
