#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import datetime
from time import time

from Config import config

from gdata.client import RequestError as GDRequestError

from Libs import Client
from Libs import Database
from Libs import Folder
from Libs import Share
from Libs import Sync
from Libs import Utilities

from Objects.Enrollment import Enrollment
from Objects import ObjectUtilites

import sys, getopt


def main(limit=None, offset=None):
    start = time()
    conn = Database.connect()
    client = Client.create()

    count = 1

    print "******** VLACS CLASS FOLDERS ********"
    print "Verifying database and root folders exist..."
    check_structure(client, conn)

    print "Marking items that need to be archived..."
    set_to_archived(conn, client)

    print "Comparing the database with Google Drive..."
    cid, rid, aid = compare_db_with_drive(client, conn, limit, offset)

    if cid:
        print "--- Creating folders in Drive..."
        create_in_drive(conn, client, cid, count, offset)
    else:
        print "--- No folders to create."

    if rid:
        print "--- Renaming folders in Drive..."
        rename_in_drive(client, rid)
    else:
        print "--- Nothing to rename."

    if aid:
        print "--- Archiving folders in Drive..."
        archive_in_drive(conn, client, aid)
    else:
        print "--- Nothing to archive."

    elapsed = int(time() - start)
    print "Finished in %s" % str(datetime.timedelta(seconds=elapsed))
    
    conn.close()

def check_structure(client, conn):
    tables_exist = False
    folder_list = {}
    exists_list_gd = {}
    exists_list_db = {}
    everything_exists = False

    print "Making sure the database tables exist..."
    # CHECK FOR DATABASE TABLES #
    tables_query = Database.get(Database.execute(conn, "SELECT COUNT(*) FROM pg_tables WHERE schemaname='public' AND tablename LIKE 'vlacs%'"))
    if tables_query['count'] > 1:
        print "Database tables exist."
        tables_exist = True

    if not tables_exist:
        print "Database tables do not exist, creating..."
        Database.insert(conn, "CREATE TABLE IF NOT EXISTS vlacs_class_folders_structure(id serial, class_id integer, student_id integer, folder_name text, folder_id text, folder_parent text, isactive int DEFAULT 1 NOT NULL)")
        Database.insert(conn, "CREATE TABLE IF NOT EXISTS vlacs_class_folders_shared(id serial, folder_id text, folder_name text, shared_with text, shared_permission text)")

    print "Making sure the root folders exist in Google Drive..."
    # CHECK FOR ROOT LEVEL FOLDERS IN GOOGLE DRIVE #
    for resource in client.GetAllResources(uri="/feeds/default/private/full/root/contents/-/folder", show_root=True):
        if resource.GetResourceType() == 'folder':
            folder_list[resource.title.text] = resource.resource_id.text

    for title, f_id in folder_list.items():
        if title == config.ROOT_CLASS_FOLDER:
            print .green("--- %s exists in Google Drive." % config.ROOT_CLASS_FOLDER)
            exists_list_gd["root"] = True
        elif title == config.TEACHER_SHARE_FOLDER:
            print .green("--- %s exists in Google Drive." % config.TEACHER_SHARE_FOLDER)
            exists_list_gd["teacher"] = True
        elif title == config.STUDENT_SHARE_FOLDER:
            print .green("--- %s exists in Google Drive." % config.STUDENT_SHARE_FOLDER)
            exists_list_gd["student"] = True

    print "Making sure the database has entries for the root folders..."
    # CHECK FOR ROOT LEVEL FOLDERS IN DATABASE #
    rcf_query = Database.get(Database.execute(conn, "SELECT count(*) FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % config.ROOT_CLASS_FOLDER))
    ts_query = Database.get(Database.execute(conn, "SELECT count(*) FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % config.TEACHER_SHARE_FOLDER))
    ss_query = Database.get(Database.execute(conn, "SELECT count(*) FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % config.STUDENT_SHARE_FOLDER))

    if rcf_query['count'] > 0:
        print "--- %s exists in the Database." % config.ROOT_CLASS_FOLDER
        exists_list_db["root"] = True
    if ts_query['count'] > 0:
        print "--- %s exists in the Database." % config.TEACHER_SHARE_FOLDER
        exists_list_db["teacher"] = True
    if ss_query['count'] > 0:
        print "--- %s exists in the Database." % config.STUDENT_SHARE_FOLDER
        exists_list_db["student"] = True

    if ("root" in exists_list_db and "root" in exists_list_gd and 
            "teacher" in exists_list_db and "teacher" in exists_list_gd and 
            "student" in exists_list_db and "student" in exists_list_gd):
        everything_exists = True

    if not everything_exists:
        print "Something is missing..."
        # COMPARE AND INSERT / CREATE #
        if 'root' in exists_list_db and 'root' not in exists_list_gd:
            print "--- Root folder is in the database, but not Google Drive. Fixing..."
            rcf = Folder.create(False, client, config.ROOT_CLASS_FOLDER)
            Database.insert(conn, "UPDATE vlacs_class_folders_structure SET folder_id = '%s' WHERE folder_name = '%s'" % (rcf.resource_id.text, config.ROOT_CLASS_FOLDER))
        elif 'root' in exists_list_gd and 'root' not in exists_list_db:
            print "--- Root folder is in Google Drive but not in the database. Fixing..."
            Database.insert(conn, Database.structure_insert_string(config.ROOT_CLASS_FOLDER, folder_list[config.ROOT_CLASS_FOLDER]))
        elif 'root' not in exists_list_db and 'root' not in exists_list_gd:
            print "--- Root folder is not in Google Drive or the database. Fixing..."
            rcf = Folder.create(conn, client, config.ROOT_CLASS_FOLDER)

        if 'teacher' in exists_list_db and 'teacher' not in exists_list_gd:
            print "--- Teacher folder is in the database, but not Google Drive. Fixing..."
            rcf = Folder.create(False, client, config.TEACHER_SHARE_FOLDER)
            Database.insert(conn, "UPDATE vlacs_class_folders_structure SET folder_id = '%s' WHERE folder_name = '%s'" % (rcf.resource_id.text, config.TEACHER_SHARE_FOLDER))
        elif 'teacher' in exists_list_gd and 'teacher' not in exists_list_db:
            print "--- Teacher folder is in Google Drive but not in the database. Fixing..."
            Database.insert(conn, Database.structure_insert_string(config.TEACHER_SHARE_FOLDER, folder_list[config.TEACHER_SHARE_FOLDER]))
        elif 'teacher' not in exists_list_db and 'teacher' not in exists_list_gd:
            print "--- Teacher folder is not in Google Drive or the database. Fixing..."
            rcf = Folder.create(conn, client, config.TEACHER_SHARE_FOLDER)

        if 'student' in exists_list_db and 'student' not in exists_list_gd:
            print "--- Student folder is in the database, but not Google Drive. Fixing..."
            rcf = Folder.create(False, client, config.STUDENT_SHARE_FOLDER)
            Database.insert(conn, "UPDATE vlacs_class_folders_structure SET folder_id = '%s' WHERE folder_name = '%s'" % (rcf.resource_id.text, config.STUDENT_SHARE_FOLDER))
        elif 'student' in exists_list_gd and 'student' not in exists_list_db:
            print "--- Student folder is in Google Drive but not in the database. Fixing..."
            Database.insert(conn, Database.structure_insert_string(config.STUDENT_SHARE_FOLDER, folder_list[config.STUDENT_SHARE_FOLDER]))
        elif 'student' not in exists_list_db and 'student' not in exists_list_gd:
            print "--- Student folder is not in Google Drive or the database. Fixing..."
            rcf = Folder.create(conn, client, config.STUDENT_SHARE_FOLDER)

def compare_db_with_drive(client, conn, limit, offset):
    enrollments = Database.get(Database.execute(conn, Database.enrollment_query_string(limit=limit, offset=offset)))
    database_contents = Database.get(Database.execute(conn, Database.compare_query_string()))
    gd_root_folders = {}
    gd_contents = {}
    create_in_drive = {}
    rename_in_drive = {} 
    archive_in_drive = {}

    # STORE RESOURCE ID BY TITLE FOR ROOT FOLDERS #
    gd_root_folders = Folder.list_sub_folders(client, "root")

    # STORE LIST OF CONTENTS (TITLE BY ID) FROM ROOT FOLDER #
    gd_contents = Folder.list_sub_folders(client, gd_root_folders[config.ROOT_CLASS_FOLDER])

    # REMOVE SYNCED ENROLLMENTS FROM DICT #
    enrollments = [enrollment for enrollment in enrollments if Sync.not_synced(enrollment, database_contents)]
    
    # REMOVE ENROLLMENTS THAT NEED TO BE ARCHIVED FROM DICT #
    archive_in_drive = [enrollment for enrollment in enrollments if Sync.should_archive(enrollment, database_contents)]
    archive_in_drive = ObjectUtilites.enrollment_list_from_dict(archive_in_drive)
    # REMOVE ENROLLMENTS THAT NEED RENAMING FROM DICT #
    rename_in_drive = [enrollment for enrollment in enrollments if Sync.student_needs_renaming(enrollment, database_contents)]
    rename_in_drive = ObjectUtilites.enrollment_list_from_dict(rename_in_drive)
    # REMOVE ENROLLMENTS THAT NEED TO BE CREATED FROM DICT #
    create_in_drive = [enrollment for enrollment in enrollments if enrollment not in rename_in_drive and enrollment not in archive_in_drive]
    create_in_drive = ObjectUtilites.enrollment_list_from_dict(create_in_drive)

    return create_in_drive, rename_in_drive, archive_in_drive

def create_in_drive(conn, client, enrollments, count, offset):
    if offset != None:
        offset = int(offset)
        count = offset

    last_disp = len(enrollments)
    if offset != None:
        last_disp = len(enrollments) + offset

    for enrollment in enrollments:
        try:
            print("Processing enrollment %s/%s..." % (count, last_disp))

            folder_exists = Database.get(Database.execute(conn, Database.folder_exists_query_string(enrollment.course.id)))
            rootclassfolder_id = Database.get(Database.execute(conn, query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % (config.ROOT_CLASS_FOLDER)))
            
            if folder_exists:
                if isinstance(folder_exists, list):
                    folder_exists = folder_exists[0]
                print "Creating Student Folder: %s" % Utilities.gen_title(enrollment, "s")
                studentfolder = Folder.create_flat(conn, client, Utilities.gen_title(enrollment, "s"), rootclassfolder_id['folder_id'], folder_exists['folder_id'], enrollment.course.id, enrollment.student.id)
            else:
                title = Utilities.gen_title(enrollment, "c")
                print "Creating Class Folder: %s" % title
                classfolder = Folder.create_flat(conn, client, title, rootclassfolder_id['folder_id'], rootclassfolder_id['folder_id'], enrollment.course.id)
                print "Creating Student Folder: %s" % Utilities.gen_title(enrollment, "s")
                studentfolder = Folder.create_flat(conn, client, Utilities.gen_title(enrollment, "s"), rootclassfolder_id['folder_id'], classfolder.resource_id.text, enrollment.course.id, enrollment.student.id)
            count += 1

        except GDRequestError as e:
            print "ERROR:", e.status
            count += 1

def rename_in_drive(client, enrollments):
    for enrollment in enrollments:
        folder = client.GetResourceById(enrollment.folder_id)
        
        print "Renaming folder %s to %s..." % (folder.text.title, enrollment.folder_name)
        
        folder.title.text = enrollment.folder_name
        client.UpdateResource(folder)

def archive_in_drive(client, enrollments):
    #loop through enrollments
    #remove folder from teacher and student share structure.
    pass

def set_to_archived(conn, client):
    enrollments = Database.get(Database.execute(conn, Database.enrollment_query_string()))
    database_contents = Database.get(Database.execute(conn, Database.compare_query_string()))

    items_to_archive = {}

    items_to_archive = [entry for entry in database_contents if Sync.not_exists_in_enrollments(entry, enrollments)]

    for entry in items_to_archive:
        Database.set_entry_to_archived(conn, entry)

def check_for_class_rename(conn, client):
    pass

if __name__ == "__main__":
    limit = None
    offset = None
    redirect_output = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hl:o:f:",["help","limit=","offset=","file="])
    except getopt.GetoptError:
        print 'run_flat_batch.py [-l <limit> -o <offset> -f <output file>]'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'run_flat_batch.py [-l <limit> -o <offset> -f <output file>]'
            sys.exit()
        elif opt in ("-l", "--limit"):
            limit = arg
        elif opt in ("-o", "--offset"):
            offset = arg
        elif opt in ("-f", "--file"):
            redirect_output = arg

    if not redirect_output:
        main(limit=limit, offset=offset)
    else:
        print "Running..."
        with Utilities.redirect_stdout(redirect_output):
            main(limit=limit, offset=offset)

        print "Finished, output stored in %s" % (redirect_output)