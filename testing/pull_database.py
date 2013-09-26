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
		cursor.execute("SELECT * FROM view_vlacs_class_folders LIMIT(%s)" % (limit))

	for row in cursor:
		print_row(row)

	conn.close()

def print_row(row):
	WHITE   = "\033[0m"
	GREEN   = "\033[92m"

	print("--------------------------------------------------------------------------------------")
	print("%sStudent Name: %s%-30s%sStudent Email: %s%-30s" % (GREEN, WHITE, row['student_firstname'] + " " + row['student_lastname'], GREEN, WHITE, row['student_email']))
	print("%sClass:        %s%-30s%sClass ID:      %s%-30s" % (GREEN, WHITE, row['course_name'], GREEN, WHITE, row['class_id'])) 
	print("%sTeacher Name: %s%-30s%sTeacher Email: %s%-30s" % (GREEN, WHITE, row['teacher_firstname'] + " " + row['teacher_lastname'], GREEN, WHITE, row['teacher_email']))

if __name__ == "__main__":
	main(sys.argv[1])
