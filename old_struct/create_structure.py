#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Libs import Client
from Libs import Database
from Libs import Folder
from Config import config

def main():
    conn = Database.connect()
    Database.insert(conn, "CREATE TABLE IF NOT EXISTS vlacs_class_folders_structure(id serial, class_id integer, folder_name text, folder_id text, folder_parent text);")
    Database.insert(conn, "CREATE TABLE IF NOT EXISTS vlacs_class_folders_shared(id serial, folder_id text, shared_email text, shared_permission text);")
    conn.close()
    
    #Create gdata client object
    client = Client.create()

    Folder.create(client, config.ROOT_ARCHIVE_FOLDER)
    Folder.create(client, config.ROOT_CLASS_FOLDER)

if __name__ == "__main__":
    main()
