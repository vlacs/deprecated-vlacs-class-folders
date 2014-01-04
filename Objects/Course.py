#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

class Course:
	""" Course object.

	Contains the proper structure for a course,
	this object is primarily used within the Enrollment object.
	"""
	def __init__(self, id=None, name=None, version=None):
		self.id      = id
		self.name    = name
		self.version = version