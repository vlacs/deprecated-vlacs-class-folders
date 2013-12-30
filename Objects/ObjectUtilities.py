#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Enrollment import Enrollment

def enrollment_list_from_dict(db_result_dict):
	return_list = []

	for enrollment in db_result_dict:
		tmp_enr = Enrollment()

		tmp_enr.master_id = enrollment['master_id']
		tmp_enr.course = Course(enrollment['course_id'],
			                 enrollment['course_name'],
			                 Utilities.course_version(enrollment['course_full_name']))

		tmp_enr.student = Student(enrollment['student_id'],
							   enrollment['student_firstname'],
							   enrollment['student_lastname'],
							   enrollment['student_email'])

		tmp_enr.teacher = Teacher(enrollment['teacher_id'],
			                   enrollment['teacher_firstname'],
			                   enrollment['teacher_lastname'],
			                   enrollment['teacher_email'])
		return_list.append(tmp_enr)

	return return_list