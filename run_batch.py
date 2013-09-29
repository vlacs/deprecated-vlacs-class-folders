#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Classes import Database
from Classes import Client

def main():
	result = Database.get(limit=30)
	cursor = result['cursor']
	client = Client.create()

	count = 1

	for row in cursor:
		print "Processing row %s / %s..." % (count, len(cursor))
		check_db = Database.get(query="SELECT class_id, folder_id FROM vlacs_class_folders_structure WHERE class_id = '%s'" % (result['class_id']))
		if len(check_db > 0):
			classfolder_id = Database.get(query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = 'VLACS Class Folders'")
			archive_id = Database.get(query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = 'VLACS Archive'")
			
			classfolder = Folder.create(client, row['course_name'] + " - " + row['teacher_firstname'] + " " + row['teacher_lastname'] + " - " + row['class_id'], classfolder_id['folder_id'])
			Folder.create(client, row['course_name'] + " - " + row['teacher_firstname'] + " " + row['teacher_lastname'] + " - " + row['class_id'], archive_id['folder_id'])
			Folder.create(client, row['student_lastname'] + ", " + row['student_firstname'] + " - Assignments", classfolder.resource_id.text)
		else:
			Folder.create(client, row['student_lastname'] + ", " + row['student_firstname'] + " - Assignments", check_db['folder_id'])
		count += 1

	Database.close(result['connection'])

if __name__ == "__main__":
	main()