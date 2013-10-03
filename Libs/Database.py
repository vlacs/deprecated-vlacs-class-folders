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
    elif limit != None:
        query_string = "SELECT * FROM view_vlacs_class_folders LIMIT(%s)" % (limit)
    elif offset != None:
        query_string = "SELECT * FROM view_vlacs_class_folders OFFSET(%s)" % (offset)
    return query_string

def folder_exists_query_string(class_id):
    query_string = "SELECT class_id, folder_id FROM vlacs_class_folders_structure WHERE class_id = %s" % (class_id)
    return query_string

def execute(conn, query):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(query)
    return cursor

def get(cursor):
    results = cursor.fetchall()
    cursor.close
    print "DEBUG: results = %s" % results
    if len(results) < 1:
        return False
    elif len(results) > 1:
        return results
    else:
        getone(results)

def getone(result_list):
    return result_list[0]