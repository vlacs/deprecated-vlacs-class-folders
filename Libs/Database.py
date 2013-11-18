#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import sys

from Config import config
import psycopg2
import psycopg2.extras


def connect():
    conn = psycopg2.connect(host=config.DATABASE['host'], user=config.DATABASE['user'],
        password=config.DATABASE['password'], database=config.DATABASE['database'])
    return conn

def enrollment_query_string(limit=None, offset=None, where=None):
    query_string = "SELECT * FROM view_vlacs_class_folders"
    if where != None:
        query_string = "SELECT * FROM view_vlacs_class_folders WHERE %s" % (where)

        
    if limit != None and offset != None:
        query_string = "SELECT * FROM view_vlacs_class_folders LIMIT(%s) OFFSET(%s)" % (limit, offset)
    elif limit != None:
        query_string = "SELECT * FROM view_vlacs_class_folders LIMIT(%s)" % (limit)
    elif offset != None:
        query_string = "SELECT * FROM view_vlacs_class_folders OFFSET(%s)" % (offset)
    return query_string

def compare_query_string():
    query_string = "SELECT * FROM vlacs_class_folders_structure"
    return query_string

def folder_exists_query_string(class_id):
    query_string = "SELECT class_id, folder_id FROM vlacs_class_folders_structure WHERE class_id = %s" % (class_id)2
    return query_string

def structure_insert_string(folder_name, folder_id, folder_parent=None, class_id=None, student_id=None):
    if folder_parent != None and class_id != None and student_id != None:
        insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id, folder_parent, class_id, student_id) VALUES ('%s', '%s', '%s', '%s', '%s')" % (folder_name, folder_id, folder_parent, class_id, student_id)
    elif folder_parent != None and class_id != None:
        insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id, folder_parent, class_id) VALUES ('%s', '%s', '%s', '%s')" % (folder_name, folder_id, folder_parent, class_id)
    elif class_id != None and student_id != None:
        insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id, class_id, student_id) VALUES ('%s', '%s', '%s', '%s')" % (folder_name, folder_id, class_id, student_id)
    elif folder_parent != None and student_id != None:
        insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id, folder_parent, student_id) VALUES ('%s', '%s', '%s', '%s')" % (folder_name, folder_id, folder_parent, student_id)
    elif folder_parent != None:
        insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id, folder_parent) VALUES ('%s', '%s', '%s')" % (folder_name, folder_id, folder_parent)
    elif class_id != None:
        insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id, class_id) VALUES ('%s', '%s', '%s')" % (folder_name, folder_id, class_id)
    elif student_id != None:
        insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id, student_id) VALUES ('%s', '%s', '%s')" % (folder_name, folder_id, student_id)
    else:
        insert_string = "INSERT INTO vlacs_class_folders_structure (folder_name, folder_id) VALUES ('%s', '%s')" % (folder_name, folder_id)

    return insert_string

def set_entry_to_archived(conn, entry):
    execute(conn, "UPDATE vlacs_class_folders_structure SET isactive = 0 WHERE class_id = '%s' AND student_id = '%s' AND folder_name = '%s' AND folder_id = '%s' AND folder_parent = '%s'" % (entry['class_id'], entry['student_id'], entry['folder_name'], entry['folder_id'], entry['folder_parent']))

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
    elif len(results) > 1:
        return results
    else:
        return getone(results)

def getone(result_list):
    return result_list[0]