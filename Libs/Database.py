#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import sys
import psycopg2
import psycopg2.extras
from Config import config

def connect():
    conn = psycopg2.connect(host=config.DATABASE['host'], user=config.DATABASE['user'],
        password=config.DATABASE['password'], database=config.DATABASE['database'])
    return conn

def enrollment_query_string(limit=None, offset=None):
    query_string = "SELECT * FROM view_vlacs_class_folders"
    if limit != None and offset != None:
        query_string = "SELECT * FROM view_vlacs_class_folders LIMIT(%s) OFFSET(%s)" % (limit, offset)
        print query_string
    elif limit != None:
        query_string = "SELECT * FROM view_vlacs_class_folders LIMIT(%s)" % (limit)
    elif offset != None:
        query_string = "SELECT * FROM view_vlacs_class_folders OFFSET(%s)" % (offset)
    return query_string

def compare_query_string(limit=None, offset=None):
    query_string = "SELECT * FROM vlacs_class_folders_structure"
    if limit != None and offset != None:
        query_string = "SELECT * FROM vlacs_class_folders_structure LIMIT(%s) OFFSET(%s)" % (limit, offset)
        print query_string
    elif limit != None:
        query_string = "SELECT * FROM vlacs_class_folders_structure LIMIT(%s)" % (limit)
    elif offset != None:
        query_string = "SELECT * FROM vlacs_class_folders_structure OFFSET(%s)" % (offset)
    return query_string

def folder_exists_query_string(class_id):
    query_string = "SELECT class_id, folder_id FROM vlacs_class_folders_structure WHERE class_id = %s" % (class_id)
    return query_string

def two_value_structure_insert_string(folder_name, folder_id):
    insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id) VALUES ('%s', '%s');" % (folder_name, folder_id)
    return insert_string

def parent_structure_insert_string(folder_name, folder_id, folder_parent):
    insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id, folder_parent) VALUES ('%s', '%s', '%s');" % (folder_name, folder_id, folder_parent)
    return insert_string

def class_id_structure_insert_string(folder_name, folder_id, class_id):
    insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id, class_id) VALUES ('%s', '%s', '%s');" % (folder_name, folder_id, class_id)
    return insert_string

def parent_class_id_structure_insert_string(class_id, folder_name, folder_id, folder_parent):
    insert_string = "INSERT INTO vlacs_class_folders_structure (class_id, folder_name, folder_id, folder_parent) VALUES ('%s', '%s', '%s', '%s');" % (class_id, folder_name, folder_id, folder_parent)
    return insert_string

def execute(conn, query):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(query)
    return cursor

def insert(conn, statement):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(statement)
    conn.commit()
    cursor.close()

def get(cursor):
    results = cursor.fetchall()
    cursor.close
    if len(results) < 1:
        return False
    else:
        return results