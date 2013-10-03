#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import string

def clean_title(title):
	clean = title
	clean = string.capwords(clean)
	clean = string.replace(clean, "'", "''")

	return clean