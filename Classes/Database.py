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

def get(query="e", limit="e"):
	conn = connect()
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	if query == "e":
		if limit == "e":
			cursor.execute("SELECT * FROM view_vlacs_class_folders")
		else:
			cursor.execute("SELECT * FROM view_vlacs_class_folders LIMIT(%s)" % (limit))
	else:
		if limit == "e":
			cursor.execute(query)
		else:
			cursor.execute("%s LIMIT(%s)", query, limit)

	return cursor