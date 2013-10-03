#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import string

def clean_title(title):
	clean = title
	clean = string.replace(clean, "'", "''")

	return clean

def clean_name(name):
	clean = name
	clean = string.capitalize(clean)

	return clean

def course_version(course_full_name):
	course_version = course_full_version
	course_version = course_version.split("-")
	course_version = course_version[1].split("_")

	return course_version[0]