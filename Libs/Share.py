#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Config import config

def share(client, conn, folder_res_id, share_with, permission):
    pass

def create_share_structure():
	pass

def unshare(client, conn, folder_res_id, unshare_with):
    pass

def remove_share_structure():
	pass

def retrieve_share_structures():
	structures = {}

	teacher = config.TEACHER_SHARE_STRUCTURE
	teacher_alt = config.ALT_TEACHER_SHARE_STRUCTURE
	student = config.STUDENT_SHARE_STRUCTURE
	student_alt = config.ALT_STUDENT_SHARE_STRUCTURE

	if teacher != "":
		structures['teacher'] = parse_share_structure_string(teacher)
	if teacher_alt != "":
		structures['teacher_alt'] = parse_share_structure_string(teacher_alt)
	if student != "":
		structures['student'] = parse_share_structure_string(student)
	if student_alt != "":
		structures['student_alt' = parse_share_structure_string(student_alt)

	return structures

def parse_share_structure_string(structure):
	structure_out = {}
	structure_in = structure.split('/');

	level = 0

	for item in structure_in:
		if "}}{{" in item:
			multiple = item.split('}{')
			for entry in multiple:
				if '{{' in entry:
					name = entry + "}"
					structure_out[name] = level
				else
					name = "{" + entry
					structure_out[name] = level
		else:
			structure_out[name] = level
		level += 1

	return structure_out