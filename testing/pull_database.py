#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import sys
import config
import psycopg2
import psycopg2.extras

def main(limit="e"):
	conn = psycopg2.connect(host=config.DATABASE['host'], user=config.DATABASE['user'], 
		password=config.DATABASE['password'], database=config.DATABASE['database'])
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	if limit == "e":
		cursor.execute("SELECT * FROM view_vlacs_class_folders")
	else:
		cursor.execute("SELECT * FROM view_vlacs_class_folders LIMIT(" + limit + ")")

	for row in cursor:
		print("\033[92mStudent Name:\033[0m %-20s\033[92m Email:\033[0m %-31s\033[34mClass:\033[0m %-10s\033[34m Class ID:\033[0m %-6s\033[31mTeacher Name:\033[0m %-30s\033[31mTeacher Email:\033[0m  %-20s" % 
			(row['student_firstname'] + " " + row['student_lastname'], row['student_email'], 
			row['course_name'], row['class_id'], row['teacher_firstname'] + " " + row['teacher_lastname'],
			row['teacher_email']))

	conn.close()

if __name__ == "__main__":
	main(sys.argv[1])
