#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from Config import 
from collections import OrderedDict
from Libs import Database

def share(client, conn, folder_entry, share_with, permission):
    pass

def create_share_structure(client, conn, folder_entry):
	enrollment = Database.get(Database.execute(conn, Database.enrollment_query_string(where="class_id = '" + folder_entry['class_id'] + "' AND student_id = '" + folder_entry['student_id'] + "'")))
	parent_res_id = ""

	structures = retrieve_share_structures()

	for structure in structures:
		for template, level in structure.iteritems():
			#If folder for current level exists store the resource_id.text in
			#a temp variable, then skip the creation and move on to the next level

	#Return resource_id.text from parent of {{STUDENT_ASSIGNMENTS}}
	return parent_res_id

def unshare(client, conn, folder_res_id, unshare_with):


def remove_share_structure(folder_res_id):
	#Get resource_id.text from folder parent and store in variable
    
    #Delete folder with folder_res_id

    #Recursively delete parent elements if they have no children

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
		structures['student_alt'] = parse_share_structure_string(student_alt)

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
			structure_out[item] = level
		level += 1

	return OrderedDict(sorted(structure_out.items(), key=lambda d: d[1]))