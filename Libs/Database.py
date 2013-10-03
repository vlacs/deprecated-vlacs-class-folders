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
    # TODO
    print "deleteme! (Database.execute)"
    conn = connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

# TODO: separate the SQL generation (or selection, really) from get, so it can be called like this:
# get(conn, Database.query_string(query=None, limit=None, offset=None))
# data = Database.get(Database.execute(conn, Database.query_string(query=None, limit=None, offset=None)))
# ...where query_string returns the SQL that will be used for the query,
# ...and execute does the query and returns the cursor
# ...and get does fetchall(), closes the cursor, and returns the data
# ...maybe also have get1(), which takes the first thing returned by fetchall() (assuming that's always a list)
# ...maybe also have ensure1(), which ensures that the list from fetchall() has length 1, and then calls get1(), else returns False
def get(conn, query=None, limit=None, offset=None):
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

    return cursor

def close(connection, cursor=None):
    connection.close()
    if cursor != None:
        cursor.close()
