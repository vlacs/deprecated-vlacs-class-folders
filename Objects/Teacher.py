#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

class Teacher:
	""" Teacher object.

	Contains the proper structure for a Teacher,
	this object is primarily used within the Enrollment object.
	"""
	def __init__(self, id=None, firstname=None, lastname=None, email=None):
		self.id        = id
		self.firstname = firstname
		self.lastname  = lastname
		self.email     = email