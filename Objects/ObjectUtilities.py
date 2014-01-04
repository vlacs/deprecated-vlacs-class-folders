#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Enrollment import Enrollment

def enrollment_list_from_dict(db_result_dict):
	result_list = []

	for enrollment in db_result_dict:
		tmp_enr = Enrollment()
		tmp_enr.create(enrollment)
		result_list.append(tmp_enr)

	return result_list