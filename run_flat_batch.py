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
    conn = Database.connect()
    client = Client.create()

    count = 1
    student_count = 0
    classroom_count = 0
    error_count = 0

    if offset != None:
        offset = int(offset)
        count = offset

    if limit != None:
        last_disp = limit

    enrollments = Database.get(Database.execute(conn, Database.enrollment_query_string(limit=limit, offset=offset)))
    last_disp = len(enrollments)
    if offset != None:
        last_disp = len(enrollments) + offset

    start = time()
    for enrollment in enrollments:
        try:
            print("Processing enrollment %s/%s..." % (count, last_disp))
            if(Utilities.check_nulls(enrollment)):
                folder_exists = Database.get(Database.execute(conn, Database.folder_exists_query_string(enrollment['class_id'])))
                rootclassfolder_id = Database.get(Database.execute(conn, query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % (config.ROOT_CLASS_FOLDER)))
                
                if folder_exists:
                    print "Class Folder Found, %s..." % (Utilities.gen_title(enrollment, "c"))
                    studentfolder = Folder.create_flat(client, Utilities.gen_title(enrollment, "s"), rootclassfolder_id['folder_id'], folder_exists['folder_id'])
                    student_count += 1
                else:
                    title = Utilities.gen_title(enrollment, "c")
                    print "Class Folder not found, creating: %s" % title

                    classfolder = Folder.create_flat(client, title, rootclassfolder_id['folder_id'], rootclassfolder_id['folder_id'], enrollment['class_id'])
                    classroom_count += 1
                    studentfolder = Folder.create_flat(client, Utilities.gen_title(enrollment, "s"), rootclassfolder_id['folder_id'], classfolder.resource_id.text)
                    student_count += 1
            else:
                print "ERROR:", count, "HAS NULL VALUE(S)"
            count += 1
        except gdata.client.RequestError as e:
            print "ERROR:", e.status
            count += 1

    elapsed = time() - start
    elapsed_min = '{0:.2g}'.format(elapsed / 60)
    if offset != None:
        enrollments_min = elapsed_min / count-offset
        print "It took %s min(s) to process %s enrollments. (%s enrollments /min" % (elapsed_min, count-offset, enrollments_min)
        print "%s classrooms containing %s students were processed successfully." % (classroom_count, student_count)
    else:
        enrollments_min = elapsed_min / count
        print "It took %s min(s) to process %s enrollments." % (elapsed_min, count, enrollments_min)
        print "%s classrooms containing %s students were processed." % (classroom_count, student_count)       
    conn.close()

def sync():
    conn = Database.connect()
    db_records = Database.get(Database.execute(conn, "SELECT * FROM vlacs_class_folders_structure"))

# TODO: consider getopt() for make benefit glorious CLI
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
            inputfile = arg
        elif opt in ("-o", "--offset"):
            outputfile = arg
        else:
            limit = None
            offset = None
    print 'Limit is:', limit
    print 'Offset is:', offset