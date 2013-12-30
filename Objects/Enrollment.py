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
		self.master_id = None
		self.course = None
		self.student = None
		self.teacher = None

	def create(self, db_result):
		self.master_id = db_result['master_id']
		self.course = Course(db_result['course_id'],
			                 db_result['course_name'],
			                 Utilities.course_version(db_result['course_full_name']))

		self.student = Student(db_result['student_id'],
							   db_result['student_firstname'],
							   db_result['student_lastname'],
							   db_result['student_email'])

		self.teacher = Teacher(db_result['teacher_id'],
			                   db_result['teacher_firstname'],
			                   db_result['teacher_lastname'],
			                   db_result['teacher_email'])