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

def structure_get_folder_id_string(folder_name, class_id, student_id):
    query_string = "SELECT folder_id FROM vlacs_class_folders_structure WHERE folder_name = '%s' AND class_id = '%s' AND student_id = '%s'" % (folder_name, class_id, student_id)
    return query_string

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

def insert_if_not_exists(conn, table, cols):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    q_string = construct_query_string(table, cols)
    get = get(execute(conn, q_string))
    
    if get:
        return get
    else:
        i_string = construct_insert_string(table, cols)
        insert(conn, i_string)
        return True

def update(conn, table, cols, wheres):
    insert(conn, construct_update_string(table, cols, wheres))

def construct_insert_string(table, cols):
    i_string = "INSERT INTO %s (" % (table)

    count = 1

    #Construct query string and insert string
    for n, col in cols.iteritems():
        if count == 1:
            if len(cols) > 1:
                i_string += "%s, " % (n)
            else:
                i_string += "%s)" % (n)
            count += 1
        elif count == len(cols):
            i_string += "%s)" % (n)
            count += 1
        else:
            i_string += "%s, " % (n)
            count += 1

    for n, col in cols.iteritems():
        if count == 1:
            if col['type'] == 's':
                i_string += " VALUES ('%s'" % (col['value'])
            else:
                i_string += " VALUES (%s" % (col['value'])
            if len(cols) > 1:
                i_string += ","
            else:
                i_string += ")"
            count += 1
        elif count == len(cols):
            if col['type'] == 's':
                i_string += " '%s')" % (col['value'])
            else:
                i_string += " %s)" % (col['value'])
            count += 1
        else:
            if col['type'] == 's':
                i_string += " '%s'," % (col['value'])
            else:
                i_string += " %s," % (col['value'])
            count += 1

    return i_string

def construct_query_string(table, cols):
    q_string = "SELECT * FROM %s WHERE "

    count = 1

    for n, col in cols.iteritems():
        if count == 1:
            if col['type'] == 's':
                q_string += "%s = '%s'" % (n, col['value'])
            else:
                q_string += "%s = %s" % (n, col['value'])
            count += 1
        else:
            if col['type'] == 's':
                q_string += " AND %s = '%s'" % (n, col['value'])
            else:
                q_string += " AND %s = %s" % (n, col['value'])
            count += 1

    return q_string 

def construct_update_string(table, cols, wheres):
    u_string = "UPDATE %s SET " % (table)

    count = 1

    for n, col in cols.iteritems():
        if count == 1:
            if col['type'] == 's':
                u_string += "%s = '%s'" % (n, col['value'])
            else:
                u_string += "%s = %s" % (n, col['value'])
            count += 1
        else:
            if col['type'] == 's':
                u_string += " AND %s = '%s'" % (n, col['value'])
            else:
                u_string += " AND %s = %s" % (n, col['value'])
            count += 1

    count = 1

    for n, where in wheres.iteritems():
        if count == 1:
            if where['type'] == 's':
                u_string += "WHERE %s = '%s'" % (n, where['value'])
            else:
                u_string += "WHERE %s = %s" % (n, where['value'])
            count += 1
        else:
            if where['type'] == 's':
                u_string += " AND %s = '%s'" % (n, where['value'])
            else:
                u_string += " AND %s = %s" % (n, where['value'])
            count += 1

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