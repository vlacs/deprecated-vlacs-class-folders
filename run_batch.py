#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Classes import Database

def main():
	result = Database.get(limit=30)

	for row in result:
		print_row(row)

def print_row(row):
	WHITE   = "\033[0m"
	GREEN   = "\033[92m"

	print("--------------------------------------------------------------------------------------")
	print("%sStudent Name: %s%-30s%sStudent Email: %s%-30s" % (GREEN, WHITE, row['student_firstname'] + " " + row['student_lastname'], GREEN, WHITE, row['student_email']))
	print("%sClass:        %s%-30s%sClass ID:      %s%-30s" % (GREEN, WHITE, row['course_name'], GREEN, WHITE, row['class_id'])) 
	print("%sTeacher Name: %s%-30s%sTeacher Email: %s%-30s" % (GREEN, WHITE, row['teacher_firstname'] + " " + row['teacher_lastname'], GREEN, WHITE, row['teacher_email']))


if __name__ == "__main__":
	main()