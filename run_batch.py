#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import sys
from Classes import Database
from Classes import Client
from Classes import Folder

def main(limit_in=None, offset_in=None):
	result, conn = Database.get(limit=limit_in, offset=offset_in)
	client = Client.create()

	if offset_in != None:
		offset = int(offset_in)
		count = offset
	else:
		offset = None
		count = 1
		
	if limit_in != None:
		limit = int(limit_in)
	else:
		limit = None
		

	for row in result:
		if limit != None:
			if offset != None:
				last = int(offset_in) + int(limit_in)
				print("Processing row %s/%s..." % (count, last))
			else:
				print("Processing row %s/%s..." % (count, limit))
		else:
			print("Processing row %s..." % (count))
		cdb_query = "SELECT class_id, folder_id FROM vlacs_class_folders_structure WHERE class_id = %s;" % row['class_id']
		check_db, conn_cdb = Database.get(query=cdb_query)
		if len(list(check_db)) < 1:
			print "Class Folder not found, creating..."
			rootclassfolder_id_db, conn_rcf = Database.get(query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = 'VLACS Class Folders';")
			rootclassfolder_id = rootclassfolder_id_db.fetchone()

			classfolder = Folder.create(client, row['course_name'] + " - " + row['teacher_firstname'] + " " + row['teacher_lastname'] + " - " + row['class_id'], rootclassfolder_id['folder_id'], row['class_id'])
			Folder.create(client, row['student_lastname'] + ", " + row['student_firstname'] + " - Assignments", classfolder.resource_id.text)
			Database.close(conn_rcf, rootclassfolder_id_db)
		else:
			print "Class Folder Found..."
			#For some reason the script doesn't work without this redundant database call...
			classfolder_id_db, conn_cf = Database.get(query=cdb_query)
			classfolder_id = classfolder_id_db.fetchone()
			Folder.create(client, row['student_lastname'] + ", " + row['student_firstname'] + " - Assignments", classfolder_id['folder_id'])
			Database.close(conn_cf, classfolder_id_db)
		count += 1
	Database.close(conn_cdb, check_db)
	Database.close(conn, result)

if __name__ == "__main__":
	if len(sys.argv) > 2:
		main(sys.argv[1], sys.argv[2])
	elif len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		main()