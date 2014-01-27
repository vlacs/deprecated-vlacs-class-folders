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
    fix_structure(client, conn)

    print "Marking items that need to be archived..."
    set_to_archived(conn, client)

    print "Comparing the database with Google Drive..."
    cid, rcid, rid, aid = compare_db_with_drive(client, conn, limit, offset)

    if cid:
        print "--- Creating folders in Drive..."
        create_in_drive(conn, client, cid, count, offset)
    else:
        print "--- No folders to create."

    if rid:
        print "--- Renaming student folders in Drive..."
        rename_folder_in_drive(client, rid)
    else:
        print "--- No student folders to rename."

    if rcid:
        print "--- Renaming class folders in Drive..."
        rename_folder_in_drive(client, rcid)
    else:
        print "--- No class folders to rename."

    if aid:
        print "--- Archiving folders in Drive..."
        archive_in_drive(conn, client, aid)
    else:
        print "--- Nothing to archive."

    elapsed = int(time() - start)
    print "Finished in %s" % str(datetime.timedelta(seconds=elapsed))
    
    conn.close()

def compare_db_with_drive(client, conn, limit, offset):
    enrollments = Database.get(Database.execute(conn, Database.enrollment_query_string(limit=limit, offset=offset)))
    database_contents = Database.get(Database.execute(conn, Database.compare_query_string()))

    gd_root_folders = Folder.list_sub_folders(client, "root")
    gd_contents = Folder.list_sub_folders(client, gd_root_folders[config.ROOT_CLASS_FOLDER])

    # REMOVE SYNCED ENROLLMENTS FROM DICT #
    enrollments = [enrollment for enrollment in enrollments if Sync.not_synced(enrollment, database_contents)]
    
    # MOVE ENROLLMENTS THAT NEED TO BE ARCHIVED TO archive_in_drive #
    archive_in_drive = [enrollment for enrollment in enrollments if Sync.should_archive(enrollment, database_contents)]
    enrollments = Utilities.remove_from_list(archive_in_drive, enrollments)

    # MOVE ENROLLMENTS THAT NEED RENAMING TO rename_in_drive #
    rename_course_in_drive = [enrollment for enrollment in enrollments if Sync.course_needs_renaming(conn, enrollment)]
    rename_in_drive = [enrollment for enrollment in enrollments if Sync.student_needs_renaming(enrollment, database_contents)]
    enrollments = Utilities.remove_from_list(rename_in_drive, enrollments)
    
    # MOVE ENROLLMENTS THAT ARE LEFT NEED TO BE CREATED IN DRIVE #
    create_in_drive = enrollments
    rename_course_in_drive = Utilities.remove_from_list(create_in_drive, rename_course_in_drive)

    archive_in_drive = ObjectUtilites.enrollment_list_from_dict(archive_in_drive)
    rename_course_in_drive = ObjectUtilites.enrollment_list_from_dict(rename_course_in_drive)
    rename_in_drive = ObjectUtilites.enrollment_list_from_dict(rename_in_drive)
    create_in_drive = ObjectUtilites.enrollment_list_from_dict(create_in_drive)

    return create_in_drive, rename_course_in_drive, rename_in_drive, archive_in_drive

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

            fe_q = Database.get(Database.execute(conn, Database.folder_exists_query_string(enrollment.course.id)))
            rcf_q = Database.get(Database.execute(conn, query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % (config.ROOT_CLASS_FOLDER)))
            fe_id = fe_q['folder_id']
            rcf_id = rcf_q['folder_id']

            if folder_exists:
                if isinstance(folder_exists, list):
                    folder_exists = folder_exists[0]
                print "Creating Student Folder: %s" % Utilities.gen_title(enrollment, "s")
                studentfolder = Folder.create_flat(conn, client, Utilities.gen_title(enrollment, "s"), rcf_id, fe_id, enrollment.course.id, enrollment.student.id)
            else:
                title = Utilities.gen_title(enrollment, "c")
                print "Creating Class Folder: %s" % title
                classfolder = Folder.create_flat(conn, client, title, rcf_id, rcf_id, enrollment.course.id)
                print "Creating Student Folder: %s" % Utilities.gen_title(enrollment, "s")
                studentfolder = Folder.create_flat(conn, client, Utilities.gen_title(enrollment, "s"), rcf_id, classfolder.resource_id.text, enrollment.course.id, enrollment.student.id)
            count += 1

        except GDRequestError as e:
            print "ERROR:", e.status
            count += 1

def fix_structure(client, conn):
    tables_exist = False
    folder_list = {}
    exists_list_gd = {}
    exists_list_db = {}
    everything_exists = False

    print "Making sure the database tables exist..."
    # CHECK FOR DATABASE TABLES #
    tables_query = Database.get(Database.execute(conn, "SELECT COUNT(*) FROM pg_tables WHERE schemaname='public' AND tablename LIKE 'vlacs_class_folders%'"))
    if tables_query['count'] > 1:
        print "Database tables exist."
        tables_exist = True

    if not tables_exist:
        print "Database tables do not exist, creating..."
        Database.insert(conn, "CREATE TABLE IF NOT EXISTS vlacs_class_folders_structure(id serial, class_id integer, student_id integer, folder_name text, folder_id text, folder_parent text, isactive int DEFAULT 1 NOT NULL)")
        Database.insert(conn, "CREATE TABLE IF NOT EXISTS vlacs_class_folders_shared(id serial, folder_id text, folder_name text, shared_with text, shared_permission text)")

    print "Making sure the root folders exist in Google Drive and Database..."
    # STORE NAMES OF ROOT LEVEL FOLDERS IN LIST #
    for resource in client.GetAllResources(uri="/feeds/default/private/full/root/contents/-/folder", show_root=True):
        if resource.GetResourceType() == 'folder':
            folder_list[resource.title.text] = resource.resource_id.text

    for folder_name in [config.ROOT_CLASS_FOLDER, config.TEACHER_SHARE_FOLDER, config.STUDENT_SHARE_FOLDER]:
        # CHECK IF FOLDER EXISTS IN DRIVE #
        for title, f_id in folder_list.items():
            if title == folder_name:
                print "--- %s exists in Google Drive." % (folder_name)
                exists_list_gd[folder_name] = True

        #CHECK IF FOLDER EXISTS IN DATATBASE #
            cq = Database.get(Database.execute(conn, "SELECT count(*) FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % folder_name))
            if cq['count'] > 0:
                print "--- %s exists in the Database." % (folder_name)
                exists_list_db[folder_name] = True

    if (config.ROOT_CLASS_FOLDER in exists_list_db and config.ROOT_CLASS_FOLDER in exists_list_gd and 
            config.TEACHER_SHARE_FOLDER in exists_list_db and config.TEACHER_SHARE_FOLDER in exists_list_gd and 
            config.STUDENT_SHARE_FOLDER in exists_list_db and config.STUDENT_SHARE_FOLDER in exists_list_gd):
        everything_exists = True

    if not everything_exists:
        print "Something is missing..."
        # COMPARE AND INSERT / CREATE #
        for folder, config_f in [{'root', config.ROOT_CLASS_FOLDER}, {'teacher', config.TEACHER_SHARE_FOLDER}, {'student', config.STUDENT_SHARE_FOLDER}]:
            if folder in exists_list_db and folder not in exists_list_gd:
                print "--- %s folder is in the database, but not Google Drive. Fixing..." % (config_f)
                f = Folder.create(False, client, config_f)
                Database.insert(conn, "UPDATE vlacs_class_folders_structure SET folder_id = '%s' WHERE folder_name = '%s'" % (f.resource_id.text, config_f))
            elif folder in exists_list_gd and folder not in exists_list_db:
                print "--- %s folder is in Google Drive but not in the database. Fixing..." % (config_f)
                Database.insert(conn, Database.structure_insert_string(config_f, folder_list[config_f]))
            elif folder not in exists_list_db and folder_list not in exists_list_gd:
                print "--- %s folder is not in Google Drive or the database. Fixing..." % (config_f)
                f = Folder.create(conn, client, config_f)

def rename_folder_in_drive(client, enrollments):
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


if __name__ == "__main__":
    limit = None
    offset = None

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hl:o:",["help","limit=","offset="])
    except getopt.GetoptError:
        print 'run.py [-l <limit> -o <offset>]'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'run.py [-l <limit> -o <offset>]'
            sys.exit()
        elif opt in ("-l", "--limit"):
            limit = arg
        elif opt in ("-o", "--offset"):
            offset = arg

    main(limit=limit, offset=offset)



