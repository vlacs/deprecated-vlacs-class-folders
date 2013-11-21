#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from collections import OrderedDict

from Config import config
from Libs import Database
from Libs import Folder
from Libs import ShareTemplate

import gdata.docs.data

def create_folder(client, title, parent):
	folder = gdata.docs.data.Resource(type='folder', title=title)
	parent = client.GetResourceById(parent)
	folder = client.CreateResource(folder, collection=parent)

	return folder

def share(client, conn, folder_entry, share_with, permission):
	# Loop through share structures (bottom up) and verify ACL records
    pass

def create_share_structure(client, conn, folder_entry):
	enrollment = Database.get(Database.execute(conn, Database.enrollment_query_string(where="class_id = '" + folder_entry['class_id'] + "' AND student_id = '" + folder_entry['student_id'] + "'")))
	parent_res_id = ""
	directory_folders = None
	max_level = 0

	structures = retrieve_share_structures()

	for name, structure in structures.iteritems():
		for template, level in structure.iteritems():
			if (level > max_level):
				max_level = level
		for template, level in structure.iteritems():
			folder = ShareTemplate.get(client, conn, template, enrollment)

			if level == 0:
				directory_folders = Folder.list_sub_folders(client, folder['folder_id'])
				parent_res_id = folder['folder_id']	
			else:				
				directory_folders = Folder.list_sub_folders(client, parent_res_id)

				#Make sure the folder isn't the student assignment folder
				if not folder['isassignment']:					
					#If the folder is already there, store the resource_id and move on
					if folder['folder_name'] in directory_folders:
						print "DEBUG: Folder exists, ", directory_folders[folder['folder_name']]
						if level != max_level:
							parent_res_id = directory_folders[folder['folder_name']]
					#If the folder is not there, create it, store the id, and move on
					else:
						print "DEBUG: Creating new folder"
						new_folder = create_folder(client, folder['folder_name'], parent_res_id)
						if level != max_level:
							parent_res_id = new_folder.resource_id.text
				else:
					print "DEBUG: Copying assignment folder"
					Folder.copy(client, folder['folder_id'], parent_res_id)

	return parent_res_id

def unshare(client, conn, folder_res_id, unshare_with):
	# Loop through share structures (bottom up) and remove ACL entry for user
	pass


def remove_share_structure(folder_res_id):
	#Get resource_id.text from folder parent and store in variable
    
    #Delete folder with folder_res_id

    #Recursively delete parent elements if they have no children
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
				else:
					name = "{" + entry
					structure_out[name] = level
		else:
			structure_out[item] = level
		level += 1

	return OrderedDict(sorted(structure_out.items(), key=lambda d: d[1]))