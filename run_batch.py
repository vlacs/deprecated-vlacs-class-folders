#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Classes import Database
from Classes import Client
from Classes import Folder

def main():
	result, conn = Database.get(limit=30)
	client = Client.create()

	count = 1

	for row in result:
		print("Processing row %s..." % (count))
		cdb_query = "SELECT class_id, folder_id FROM vlacs_class_folders_structure WHERE class_id = %s;" % row['class_id']
		check_db, conn_cdb = Database.get(query=cdb_query)
		if len(list(check_db)) < 1:
			print "Class Folder not found, creating..."
			classfolder_id_db, conn_cf = Database.get(query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = 'VLACS Class Folders';")
			classfolder_id = classfolder_id_db.fetchone()

			classfolder = Folder.create(client, row['course_name'] + " - " + row['teacher_firstname'] + " " + row['teacher_lastname'] + " - " + row['class_id'], classfolder_id['folder_id'], row['class_id'])
			Folder.create(client, row['student_lastname'] + ", " + row['student_firstname'] + " - Assignments", classfolder.resource_id.text)
			Database.close(conn_cf, classfolder_id_db)
		else:
			print "Class Folder Found..."
			res = check_db.fetchall()
			if res == None:
				print check_db.rowcount, res
				break
			print res
			Folder.create(client, row['student_lastname'] + ", " + row['student_firstname'] + " - Assignments", res[0]['folder_id'])
		count += 1
	Database.close(conn_cdb, check_db)
	Database.close(conn, result)

if __name__ == "__main__":
	main()
