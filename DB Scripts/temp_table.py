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
            
            	c.execute('CREATE TABLE IF NOT EXISTS temp(noun TEXT, pnoun TEXT)')

		return c    		
	except Error as e:
        	print(e)



def main():
	conn=create_connection()
	c=create_table(conn)
    	c.close()
    	conn.close()

if __name__ =='__main__':
	main()
