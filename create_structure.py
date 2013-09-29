#!/usr/bin/python

### FOLDER STRUCTURE ###
# -VLACS Arcive
# +VLACS Class Folders
# -+Class Name - Teacher - ID
# ---Student Last Name, Student First Name - Assignments

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Classes import Client
from Classes import Database
from Classes import Folder

def main():
	Database.execute("CREATE TABLE IF NOT EXISTS vlacs_class_folders_structure(id serial, class_id integer, folder_name character(255), folder_id character(255), folder_parent character(255));")
	Database.execute("CREATE TABLE IF NOT EXISTS vlacs_class_folders_shared(id serial, folder_id integer, shared_email character(255), shared_permission character(255));")

	#Create gdata client object
	client = Client.create()

	Folder.create(client, 'VLACS Archive')
	Folder.create(client, 'VLACS Class Folders')

if __name__ == "__main__":
	main()