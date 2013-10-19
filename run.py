#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import sys, getopt
import gdata.client
from time import time
from Libs import Database
from Libs import Client
from Libs import Folder
from Libs import Utilities
from Config import config

def main(limit=None, offset=None):
    start = time()
    conn = Database.connect()
    client = Client.create()

    count = 1

    print "******** VLACS CLASS FOLDERS ********"
    print "(NI) Checking if database and folders exist.."
    # Check for database and folders

    print "(NI) Comparing the database with Google Drive..."
    # Compare database with google drive

    print "Applying changes to Google Drive..."
    enrollments = Database.get(Database.execute(conn, Database.enrollment_query_string(limit=limit, offset=offset)))
    create_in_drive(conn, enrollments, count, offset)
    # archive_in_drive for folders that no longer show in database

    elapsed = time() - start
    elapsed_min = '{0:.2g}'.format(elapsed / 60)

    print "Finished in %s mins." % elapsed_min
    
    conn.close()

def check_structure(client, conn):
    Database.insert(conn, "CREATE TABLE IF NOT EXISTS vlacs_class_folders_structure(id serial, class_id integer, folder_name text, folder_id text, folder_parent text);")
    Database.insert(conn, "CREATE TABLE IF NOT EXISTS vlacs_class_folders_shared(id serial, folder_id text, shared_email text, shared_permission text);")

    

def create_in_drive(conn, enrollments, count, offset):
    if offset != None:
        offset = int(offset)
        count = offset

    student_count = 0
    classroom_count = 0
    error_count = 0

    last_disp = len(enrollments)
    if offset != None:
        last_disp = len(enrollments) + offset

    start = time()
    for enrollment in enrollments:
        try:
            print("Processing enrollment %s/%s..." % (count, last_disp))
            if(Utilities.fix_nulls(enrollment)):
                folder_exists = Database.get(Database.execute(conn, Database.folder_exists_query_string(enrollment['class_id'])))
                rootclassfolder_id = Database.get(Database.execute(conn, query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % (config.ROOT_CLASS_FOLDER)))
                
                if folder_exists:
                    print "Creating Student Folder: %s" % Utilities.gen_title(enrollment, "s")
                    studentfolder = Folder.create_flat(client, Utilities.gen_title(enrollment, "s"), rootclassfolder_id['folder_id'], folder_exists['folder_id'])
                    student_count += 1
                else:
                    title = Utilities.gen_title(enrollment, "c")
                    print "Creating Class Folder: %s" % title
                    classfolder = Folder.create_flat(client, title, rootclassfolder_id['folder_id'], rootclassfolder_id['folder_id'], enrollment['class_id'])
                    classroom_count += 1
                    print "Creating Student Folder: %s" % Utilities.gen_title(enrollment, "s")
                    studentfolder = Folder.create_flat(client, Utilities.gen_title(enrollment, "s"), rootclassfolder_id['folder_id'], classfolder.resource_id.text)
                    student_count += 1
            else:
                print "ERROR:", count, "HAS NULL VALUE(S) THAT COULD NOT BE FIXED"
            count += 1
        except gdata.client.RequestError as e:
            print "ERROR:", e.status
            count += 1
    elapsed = time() - start
    elapsed_min = '{0:.2g}'.format(elapsed / 60)
    if offset != None:
        enrollments_min = elapsed_min / count-offset
        print "It took %s min(s) to process %s enrollments. (%s enrollments /min)" % (elapsed_min, count-offset, enrollments_min)
        print "%s classrooms containing %s students were processed successfully." % (classroom_count, student_count)
    else:
        enrollments_min = elapsed_min / count
        print "It took %s min(s) to process %s enrollments. (%s enrollments /min)" % (elapsed_min, count, enrollments_min)
        print "%s classrooms containing %s students were processed." % (classroom_count, student_count)

def sync():
    conn = Database.connect()
    db_records = Database.get(Database.execute(conn, "SELECT * FROM vlacs_class_folders_structure"))

if __name__ == "__main__":
    limit = None;
    offset = None;
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hl:o:",["help","limit=","offset="])
    except getopt.GetoptError:
        print 'run_flat_batch.py [-l <limit> -o <offset>]'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'run_flat_batch.py [-l <limit> -o <offset>]'
            sys.exit()
        elif opt in ("-l", "--limit"):
            limit = arg
        elif opt in ("-o", "--offset"):
            offset = arg
    main(limit=limit, offset=offset)