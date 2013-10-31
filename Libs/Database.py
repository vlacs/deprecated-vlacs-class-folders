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

def compare_query_string():
    query_string = "SELECT * FROM vlacs_class_folders_structure"
    return query_string

def folder_exists_query_string(class_id):
    query_string = "SELECT class_id, folder_id FROM vlacs_class_folders_structure WHERE class_id = %s" % (class_id)
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
        return results

def getone(result_list):
    return result_list[0]