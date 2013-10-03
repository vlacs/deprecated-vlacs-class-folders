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

def execute(query):
    conn = connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def get(query=None, limit=None, offset=None):
    conn = connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if query == None:
        if limit == None and offset == None:
            cursor.execute("SELECT * FROM view_vlacs_class_folders;")
        elif offset == None:
            cursor.execute("SELECT * FROM view_vlacs_class_folders LIMIT(%s);" % (limit))
        elif limit == None:
            cursor.execute("SELECT * FROM view_vlacs_class_folders OFFSET(%s);" % (offset))
        else:
            cursor.execute("SELECT * FROM view_vlacs_class_folders LIMIT(%s) OFFSET(%s);" % (limit, offset))
    else:
        if limit == None and offset == None:
            cursor.execute(query)
        elif offset == None:
            cursor.execute("%s LIMIT(%s);" % (query, limit))
        elif limit == None:
            cursor.execute("%s OFFSET(%s);" % (query, offset))
        else:
            cursor.execute("%s LIMIT(%s) OFFSET(%s);" % (query, limit, offset))

    return cursor, conn

def close(connection, cursor=None):
    connection.close()
    if cursor != None:
        cursor.close()
