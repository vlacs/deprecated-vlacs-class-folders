#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import config
import psycopg2
import psycopg2.extras

def main():
	conn = psycopg2.connect(host=config.DATABASE['host'], user=config.DATABASE['user'], 
							password=config.DATABASE['password'], database=config.DATABASE['database'])
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM view_vlacs_class_folders LIMIT(20)")

	k = list(cursor.keys())
	print k
	#for row in cursor:
	#	print("First Name: %s Last Name: %s Class: %s", row['student_first_name'], 
	#						row['student_last_name'], row['course_name'])

	conn.close()

if __name__ == "__main__":
	main()