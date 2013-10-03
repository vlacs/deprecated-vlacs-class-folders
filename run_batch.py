#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import sys
from Classes import Database
from Classes import Client
from Classes import Folder
from Classes import Utilities

def main(limit=None, offset=None):
    conn = Database.connect()
    client = Client.create()

    count = 1
    if offset != None:
        offset = int(offset)
        count = offset

    last_disp = "-"
    if limit != None:
        limit = int(limit)
        last_disp = limit

    if limit != None and offset != None:
        last_disp = offset + limit

    enrollments = Database.get(Database.execute(conn, Database.query_string(limit=limit, offset=offset)))
    for enrollment in enrollments:
        print("Processing enrollment %s/%s..." % (count, last_disp))
        cdb_query = "SELECT class_id, folder_id FROM vlacs_class_folders_structure WHERE class_id = %s;" % enrollment['class_id']
        folder_exists = Database.ensure1(Database.execute(conn, Database.query_string(query=cdb_query)))
        # TODO: check whether list(cur) consumes what the cursor contains
        if folder_exists:
            print "Class Folder Found..."
            Folder.create(client, Utilities.clean_name(enrollment['student_lastname']) + ", " + Utilities.clean_name(enrollment['student_firstname']) + " - Assignments", folder_exists['folder_id'])
        else:
            # TODO: get folder title here (see Utilities.title() below :), and display it
            print "Class Folder not found, creating: %s" % title
            # TODO: make "VLACS Class Folders" a configurable setting
            # TODO: remove semicolon if it's unnecessary?
            rootclassfolder_id = Database.get1(Database.execute(conn, query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = 'VLACS Class Folders';"))

            # TODO: create a function that creates the title, given a enrollment. E.g.: Utilities.title(enrollment)
            classfolder = Folder.create(client, enrollment['course_name'] + " - " + Utilities.clean_name(enrollment['teacher_firstname']) + " " + Utilities.clean_name(enrollment['teacher_lastname']) + " - " + Utilities.course_version(enrollment['course_full_name']) + " - " + enrollment['class_id'], rootclassfolder_id['folder_id'], enrollment['class_id'])
            # TODO: see above WRT Utilities.title(enrollment)
            Folder.create(client, Utilities.clean_name(enrollment['student_lastname']) + ", " + Utilities.clean_name(enrollment['student_firstname']) + " - Assignments", classfolder.resource_id.text)
        count += 1
    # TODO: do all the cursors need to be closed explicitly as well?
    Database.close(conn)

# TODO: consider getopt() for make benefit glorious CLI
if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
