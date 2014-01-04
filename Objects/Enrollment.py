#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Course import Course
from Student import Student
from Teacher import Teacher

from Libs import Utilities

class Enrollment:
	"""Enrollment object.

	Contains the proper structure for an enrollment
	there are no arguments and the enrollment can be generated
	from a dictionary returned by a database query using the create
	function
	"""
	def __init__(self):
		self.master_id   = None
		self.course      = Course()
		self.folder_id   = None
		self.folder_name = None
		self.student     = Student()
		self.teacher     = Teacher()

	def create(self, db_result):
		self.master_id         = db_result['master_id']
		
		self.course.id         = db_result['course_id']
		self.course.name       = db_result['course_name']
		self.course.version    = Utilities.course_version(db_result['course_full_name'])

		self.student.id        = db_result['student_id']
		self.student.firstname = db_result['student_firstname']
		self.student.lastname  = db_result['student_lastname']
		self.student.email     = db_result['student_email']

		self.teacher.id        = db_result['teacher_id']
		self.teacher.firstname = db_result['teacher_firstname']
		self.teacher.lastname  = db_result['teacher_lastname']
		self.teacher.email     = db_result['teacher_email']