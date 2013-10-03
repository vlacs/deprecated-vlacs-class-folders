#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import string

def clean_title(title):
	clean = title
	clean = string.replace(clean, "'", "''")

	return clean

def clean_name(name):
	clean = title
	clean = string.capitalize(clean)

	return clean