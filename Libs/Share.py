#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from collections import OrderedDict

from Config import config
from Libs import Database
from Libs import Folder
from Libs import ShareTemplate
from Libs import Utilities

from gdata.acl.data import AclRole
from gdata.acl.data import AclScope
from gdata.docs.data import AclEntry

import gdata.data
import gdata.client

import sys

def ShareFolder(client, conn, folder_entry):
    #Create the share structures and then share and modify permissions
    #for student and teacher.
    enrollment = Database.get(Database.execute(conn, Database.enrollment_query_string(where="class_id = '" + folder_entry['class_id'] + "' AND student_id = '" + folder_entry['student_id'] + "'")))
    structures = retrieve_share_structures()
    created_structures = {}
    
    print "Creating Share Structure..."

    for name, structure in structures.iteritems():
        try:
            created_structures[name] = create_share_structure(client, conn, enrollment, structure)
        except KeyError:
            print "ERROR"
            print structures
    share_roles = retrieve_share_roles(created_structures)

    print "Sharing Folders..."

    for folder in share_roles:
        # In production the teacher and student emails will come from enrollment dict
        if not folder['role']['teacher'] == 'none':
            share(client, folder['folder_id'], 'testteacher@vlacs.net', folder['role']['teacher'])
        if not folder['role']['student'] == 'none':
            share(client, folder['folder_id'], 'teststudent@vlacs.net', folder['role']['student'])

    print "Done!"

def create_share_structure(client, conn, enrollment, structure):
    parents = {}
    currentdir_folders = {}
    parsed_templates = {}
    max_level = 0
    created_structure = []

    for template, level in structure.iteritems():
        if(level > max_level):
            max_level = level
    for template, level in structure.iteritems():
        if template not in parsed_templates:
            parsed_templates[template] = ShareTemplate.get(client, conn, template, enrollment)

        folder = parsed_templates[template]
        #Create the folder in drive and set the folder id!
        if level == 0:
            #Level 0 will always be the root folders
            currentdir_folders = Folder.list_sub_folders(client, folder['folder_id'])
            cr_folder = folder_not_exists_create(client, conn, folder, template, folder['folder_id'], currentdir_folders)
            parents[level+1] = cr_folder['folder_id']
        else:
            currentdir_folders = Folder.list_sub_folders(client, parents[level])
            cr_folder = folder_not_exists_create(client, conn, folder, template, parents[level], currentdir_folders)
            parents[level+1] = cr_folder['folder_id']

        created_structure.append(cr_folder)
        dbg_arrow = '--' * level + '>'
        fmt = '{0:25}'
        print fmt.format(template), dbg_arrow, cr_folder['folder_id']

    return created_structure


def folder_not_exists_create(client, conn, folder, template, parent, currentdir_folders):
    if folder['folder_name'] in currentdir_folders:
        #folder exists, update the folder_id and return it
        folder['folder_id'] = currentdir_folders[folder['folder_name']]
        return folder
    elif folder['copy']:
        #this is a folder that needs to be copied from somewhere else
        if template == "{{STUDENT_ASSIGNMENTS}}":
            Folder.copy(client, folder['folder_id'], parent)
            return folder
        elif template == "{{CLASS_FILES}}":
            table = "vlacs_class_folders_shared"
            cols = {'folder_name':{'value':folder['folder_name'],'type':'s'}}
            class_files = Database.insert_if_not_exists(conn, table, cols)

            if class_files:
                cr_folder = Folder.create(False, client, folder['folder_name'], parent)
                cols = {'folder_id':{'value':cr_folder.resource_id.text,'type':'s'}}
                wheres = {'folder_name':{'value':folder['folder_name'],'type':'s'}}
                Database.update(conn, table, cols, wheres)
                folder['folder_id'] = cr_folder.resource_id.text
            else:
                folder['folder_id'] = class_files['folder_id']
                Folder.copy(client, folder['folder_id'], parent)
            return folder
    else:
        #folder does not exist, create it and update the folder_id and return it
        cr_folder = Folder.create(False, client, folder['folder_name'], parent)
        folder['folder_id'] = cr_folder.resource_id.text
        return folder


def parse_share_structure_string(structure):
    structure_out = {}
    structure_in = structure.split('/');

    level = 0

    for item in structure_in:
        if "}}{{" in item:
            multiple = item.split('}{')
            for entry in multiple:
                if "{{" in entry:
                    name = entry + "}"
                    structure_out[name] = level
                else:
                    name = "{" + entry
                    structure_out[name] = level
        else:
            structure_out[item] = level
        level += 1

    return OrderedDict(sorted(structure_out.items(), key=lambda d: d[1]))

def retrieve_share_roles(created_structures):
    ##
    ##    share_roles = [{'folder_id':'folder:alsdjfalksd', 'roles':{"teacher":"writer", "student":"reader"}},]
    ##
    share_roles = []
    result = []

    for name, structure in created_structures.iteritems():
        for folder in structure:
            temp_dict = {}
            temp_dict['folder_id'] = folder['folder_id']
            temp_dict['role'] = folder['role']
            share_roles.append(temp_dict)
    #Remove duplicates
    for d in share_roles:
        if d not in result:
            result.append(d)

    return result


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

def share(client, folder_id, share_with, role, try_count=1):
    folder = client.GetResourceById(folder_id)
    acl_feed = client.GetResourceAcl(folder)

    print "Sharing: %s with %s as %s, try %s" % (folder_id, share_with, role, try_count)

    try:
        for acl in acl_feed.entry:
            if acl.scope.value == share_with:
                break
        else:
            #If there is no break no acl record exists for shared_with
            acl_entry = AclEntry(
                scope = AclScope(value=share_with, type='user'),
                role = AclRole(value=role))
            client.AddAclEntry(folder, acl_entry, send_notification=False)

        if not acl.role.value == role:
            acl.role.value = role
            acl.etag = None
            client.UpdateAclEntry(acl, send_notification=False)
    except gdata.client.RequestError as e:
        # Catch the request error and retry up to three times
        # Sometimes we recieve a random 500 error and a retry
        # does the trick
        if try_count > 2:
            print "ERROR: There seems to be a problem sharing..."
            sys.exit(e.message)
        else:
            try_count += 1
            share(client, folder_id, share_with, role, try_count)

##
## TEST VARIABLES
## folder_entry = {'id':'47', 'class_id':'1463', 'student_id':'58737', 'folder_name':'Adam, Kaitlyn - Assignments', 'folder_id':'folder:0B7AqvGrb_oO8OVNwaElSdWV0ZlE', 'folder_parent':'folder:0B7AqvGrb_oO8cTdhb3BLQWEwTzQ', 'isactive':1}
##