#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import sys
import getopt
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
    if offset != None:
        offset = int(offset)
        count = offset

    last_disp = "-"
    if limit != None:
        limit = int(limit)
        last_disp = limit

    if limit != None and offset != None:
        last_disp = offset + limit

    enrollments = Database.get(Database.execute(conn, Database.enrollment_query_string(limit=limit, offset=offset)))
    start = time()
    for enrollment in enrollments:
        try:
            print("Processing enrollment %s/%s..." % (count, last_disp))
            folder_exists = Database.get(Database.execute(conn, Database.folder_exists_query_string(enrollment['class_id'])))
            rootclassfolder_id = Database.get(Database.execute(conn, query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = '%s'" % (config.ROOT_CLASS_FOLDER)))
            
            if folder_exists:
                print "Class Folder Found, %s..." % (Utilities.gen_title(enrollment, "c"))
                studentfolder = Folder.create_flat(client, Utilities.gen_title(enrollment, "s"), rootclassfolder_id['folder_id'], folder_exists['folder_id'])
            else:
                title = Utilities.gen_title(enrollment, "c")
                print "Class Folder not found, creating: %s" % title

                classfolder = Folder.create_flat(client, title, rootclassfolder_id['folder_id'], rootclassfolder_id['folder_id'], enrollment['class_id'])
                studentfolder = Folder.create_flat(client, Utilities.gen_title(enrollment, "s"), rootclassfolder_id['folder_id'], classfolder.resource_id.text)
            count += 1
        except gdata.client.RequestError as e:
            if folder_exists:
                print e.status, studentfolder
            else:
                print e.status, classfoder, studentfolder

    elapsed = time() - start
    elapsed_min = '{0:.2g}'.format(elapsed / 60)
    if offset != None:
        min_per_enrol = '{0:.2g}'.format(elapsed / (count-offset) / 60 /60)
        print "It took %s min(s) to process %s enrollments. (%s sec(s) per enrollment)" % (elapsed_min, count-offset, min_per_enrol)
    else:
        min_per_enrol = '{0:.2g}'.format(elapsed / count / 60 /60)
        print "It took %s min(s) to process %s enrollments. (%s sec(s) per enrollment)" % (elapsed_min, count, min_per_enrol)        
    conn.close()

# TODO: consider getopt() for make benefit glorious CLI
if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()