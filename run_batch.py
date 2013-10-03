#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import sys
import getopt
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
    for enrollment in enrollments:
        print("Processing enrollment %s/%s..." % (count, last_disp))
        folder_exists = Database.get(Database.execute(conn, Database.folder_exists_query_string(query=enrollment['class_id'])))
        if folder_exists:
            print "Class Folder Found..."
            Folder.create(client, Utilities.gen_title(enrollment, "s"), folder_exists['folder_id'])
        else:
            title = Utilities.gen_title(enrollment, "c")
            print "Class Folder not found, creating: %s" % title
            rootclassfolder_id = Database.get(Database.execute(conn, query="SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = ''" % (config.ROOT_CLASS_FOLDER)))

            classfolder = Folder.create(client, title, rootclassfolder_id['folder_id'], enrollment['class_id'])
            Folder.create(client, Utilities.gen_title(enrollment, "s"), classfolder.resource_id.text)
        count += 1
    conn.close()

# TODO: consider getopt() for make benefit glorious CLI
if __name__ == "__main__":
    limit = None
    offset = None

    try:
        opts, args = getopt.getopt(sys.argv, 'l:o', ['limit=', 'offset='])
    except getopt.GetoptError:
        print("Usage: python run_batch.py --limit n --offset n")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-l', '--limit'):
            limit = arg
        elif opt in ('-o', '--offset'):
            offset = arg

    main(limit, offset)