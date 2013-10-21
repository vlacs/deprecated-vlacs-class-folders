#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import sys, getopt
import gdata.client
from Config import config
from time import time
from Libs import Client
from Libs import Color
from Libs import Database
from Libs import Folder
from Libs import Utilities

def main(limit=None, offset=None):
    start = time()
    conn = Database.connect()
    client = Client.create()

    count = 1

    Color.green("******** VLACS CLASS FOLDERS ********")
    Color.blue("Verifying datbase and root folders exist...")
    check_structure(client, conn)

    Color.blue("Comparing the database with Google Drive...")
    compare_db_with_drive(client, conn)

    Color.blue("(NI) Applying changes to Google Drive...")
    #enrollments = Database.get(Database.execute(conn, Database.enrollment_query_string(limit=limit, offset=offset)))
    #create_in_drive(conn, enrollments, count, offset)
    # archive_in_drive for folders that no longer show in database

    elapsed = time() - start
    elapsed_min = '{0:.2g}'.format(elapsed / 60)

    print "Finished in %s mins." % elapsed_min
    
    conn.close()

def check_structure(client, conn):
    tables_exist = False
    folder_list = {}
    exists_list_gd = {}
    exists_list_db = {}
    everything_exists = False

    Color.cyan("Making sure the database tables exist...")
    # CHECK FOR DATBASE TABLES #
    tables_query = Database.get(Database.execute(conn, "SELECT COUNT(*) FROM pg_tables WHERE schemaname='public' AND tablename LIKE 'vlacs%'"))
    if tables_query['count'] > 1:
        Color.green("Database tables exist.")
        tables_exist = True

    if not tables_exist:
        Color.red("Database tables do not exist, creating...")
        Database.insert(conn, "CREATE TABLE IF NOT EXISTS vlacs_class_folders_structure(id serial, class_id integer, folder_name text, folder_id text, folder_parent text);")
        Database.insert(conn, "CREATE TABLE IF NOT EXISTS vlacs_class_folders_shared(id serial, folder_id text, shared_email text, shared_permission text);")

    Color.cyan("Making sure the root folders exist in Google Drive...")
    # CHECK FOR ROOT LEVEL FOLDERS IN GOOGLE DRIVE #
    for resource in client.GetAllResources(uri="/feeds/default/private/full/root/contents/-/folder", show_root=True):
        if resource.GetResourceType() == 'folder':
            folder_list[resource.title.text] = resource.resource_id.text

    for title, f_id in folder_list.items():
        if title == config.ROOT_CLASS_FOLDER:
            Color.green("--- %s exists in Google Drive." % config.ROOT_CLASS_FOLDER)
            exists_list_gd["root"] = True
        elif title == config.TEACHER_SHARE_FOLDER:
            Color.green("--- %s exists in Google Drive." % config.TEACHER_SHARE_FOLDER)
            exists_list_gd["teacher"] = True
        elif title == config.STUDENT_SHARE_FOLDER:
            Color.green("--- %s exists in Google Drive." % config.STUDENT_SHARE_FOLDER)
            exists_list_gd["student"] = True

    Color.cyan("Making sure the database has entries for the root folders...")
    # CHECK FOR ROOT LEVEL FOLDERS IN DATABASE #
    rcf_query = Database.get(Database.execute(conn, "SELECT count(*) FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % config.ROOT_CLASS_FOLDER))
    ts_query = Database.get(Database.execute(conn, "SELECT count(*) FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % config.TEACHER_SHARE_FOLDER))
    ss_query = Database.get(Database.execute(conn, "SELECT count(*) FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % config.STUDENT_SHARE_FOLDER))

    if rcf_query['count'] > 0:
        Color.green("--- %s exists in the Database." % config.ROOT_CLASS_FOLDER)
        exists_list_db["root"] = True
    if ts_query['count'] > 0:
        Color.green("--- %s exists in the Database." % config.TEACHER_SHARE_FOLDER)
        exists_list_db["teacher"] = True
    if ss_query['count'] > 0:
        Color.green("--- %s exists in the Database." % config.STUDENT_SHARE_FOLDER)
        exists_list_db["student"] = True

    if ("root" in exists_list_db and "root" in exists_list_gd and 
            "teacher" in exists_list_db and "teacher" in exists_list_gd and 
            "student" in exists_list_db and "student" in exists_list_gd):
        everything_exists = True

    if not everything_exists:
        print "Something is missing..."
        # COMPARE AND INSERT / CREATE #
        if 'root' in exists_list_db and 'root' not in exists_list_gd:
            Color.red("--- Root folder is in the database, but not Google Drive. Fixing...")
            rcf = Folder.create(conn, client, config.ROOT_CLASS_FOLDER, noDB=True)
            Database.insert(conn, "UPDATE vlacs_class_folders_structure SET folder_id = '%s' WHERE folder_name = '%s'" % (rcf.resource_id.text, config.ROOT_CLASS_FOLDER))
        elif 'root' in exists_list_gd and 'root' not in exists_list_db:
            Color.red("--- Root folder is in Google Drive but not in the database. Fixing...")
            Database.insert(conn, Database.two_value_structure_insert_string(config.ROOT_CLASS_FOLDER, folder_list[config.ROOT_CLASS_FOLDER]))
        elif 'root' not in exists_list_db and 'root' not in exists_list_gd:
            Color.red("--- Root folder is not in Google Drive or the database. Fixing...")
            rcf = Folder.create(conn, client, config.ROOT_CLASS_FOLDER)

        if 'teacher' in exists_list_db and 'teacher' not in exists_list_gd:
            Color.red("--- Teacher folder is in the database, but not Google Drive. Fixing...")
            rcf = Folder.create(conn, client, config.TEACHER_SHARE_FOLDER, noDB=True)
            Database.insert(conn, "UPDATE vlacs_class_folders_structure SET folder_id = '%s' WHERE folder_name = '%s'" % (rcf.resource_id.text, config.TEACHER_SHARE_FOLDER))
        elif 'teacher' in exists_list_gd and 'teacher' not in exists_list_db:
            Color.red("--- Teacher folder is in Google Drive but not in the database. Fixing...")
            Database.insert(conn, Database.two_value_structure_insert_string(config.TEACHER_SHARE_FOLDER, folder_list[config.TEACHER_SHARE_FOLDER]))
        elif 'teacher' not in exists_list_db and 'teacher' not in exists_list_gd:
            Color.red("--- Teacher folder is not in Google Drive or the database. Fixing...")
            rcf = Folder.create(conn, client, config.TEACHER_SHARE_FOLDER)

        if 'student' in exists_list_db and 'student' not in exists_list_gd:
            Color.red("--- Student folder is in the database, but not Google Drive. Fixing...")
            rcf = Folder.create(conn, client, config.STUDENT_SHARE_FOLDER, noDB=True)
            Database.insert(conn, "UPDATE vlacs_class_folders_structure SET folder_id = '%s' WHERE folder_name = '%s'" % (rcf.resource_id.text, config.STUDENT_SHARE_FOLDER))
        elif 'student' in exists_list_gd and 'student' not in exists_list_db:
            Color.red("--- Student folder is in Google Drive but not in the database. Fixing...")
            Database.insert(conn, Database.two_value_structure_insert_string(config.STUDENT_SHARE_FOLDER, folder_list[config.STUDENT_SHARE_FOLDER]))
        elif 'student' not in exists_list_db and 'student' not in exists_list_gd:
            Color.red("--- Student folder is not in Google Drive or the database. Fixing...")
            rcf = Folder.create(conn, client, config.STUDENT_SHARE_FOLDER)

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
                    studentfolder = Folder.create_flat(conn, client, Utilities.gen_title(enrollment, "s"), rootclassfolder_id['folder_id'], folder_exists['folder_id'])
                    student_count += 1
                else:
                    title = Utilities.gen_title(enrollment, "c")
                    print "Creating Class Folder: %s" % title
                    classfolder = Folder.create_flat(conn, client, title, rootclassfolder_id['folder_id'], rootclassfolder_id['folder_id'], enrollment['class_id'])
                    classroom_count += 1
                    print "Creating Student Folder: %s" % Utilities.gen_title(enrollment, "s")
                    studentfolder = Folder.create_flat(conn, client, Utilities.gen_title(enrollment, "s"), rootclassfolder_id['folder_id'], classfolder.resource_id.text)
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

def rename_in_drive(client, enrollments):
    pass

def compare_db_with_drive(client, conn):
    db_contents = Database.get(Database.execute(conn, Database.enrollment_query_string(limit=limit, offset=offset)))
    gd_root_folders = {}
    gd_contents = {}

    # STORE RESOURCE ID BY TITLE FOR ROOT FOLDERS #
    for resource in client.GetAllResources(uri="/feeds/default/private/full/root/contents/-/folder", show_root=True):
        if resource.GetResourceType() == 'folder':
            gd_root_folders[resource.title.text] = resource.resource_id.text

    # STORE LIST OF CONTENTS (TITLE BY ID) FROM ROOT FOLDER #
    for resource in client.GetAllResources(uri="/feeds/default/private/full/%s/contents/-/folder" % gd_root_folders[config.ROOT_CLASS_FOLDER]):
        if resource.GetResourceType() == 'folder':
            gd_contents[resource.resource_id.text] = resource.title.text

    #print gd_contents


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