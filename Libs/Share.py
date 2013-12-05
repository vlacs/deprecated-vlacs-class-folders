#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from collections import OrderedDict

from Config import config
from Libs import Database
from Libs import Folder
from Libs import ShareTemplate

import gdata.docs.data
import gdata.acl.data
import gdata.data

def create_folder(client, title, parent):
    folder = gdata.docs.data.Resource(type='folder', title=title)
    parent = client.GetResourceById(parent)
    folder = client.CreateResource(folder, collection=parent)

    return folder

def share_folder(client, conn, folder_entry):
    #Get structures and enrollment from analyze_share_structure
    enrollment, structures = analyze_share_structure(client, conn, folder_entry)
    # Loop through share structures
    for name, structure in structures.iteritems():
        for level, folder in structure.iteritems():
            #Share with student
            if 'student' in name:
                print "DEBUG: Sharing %s with student" % folder['folder_id']
                share(client, folder['folder_id'], 'teststudent@vlacs.net', folder['role']['student'])
            #Share with teacher
            if 'teacher' in name:
                print "DEBUG: Sharing %s with teacher" % folder['folder_id']
                share(client, folder['folder_id'], 'testteacher@vlacs.net', folder['role']['teacher'])

def share(client, folder_id, share_with, role):
    #list current ACL Entries and delete any for share_with
    update_acl = False
    updated = False
    folder = client.GetResourceById(folder_id)
    acl_feed = client.GetResourceAcl(folder)
    for acl in acl_feed.entry:
        if acl.scope.value == share_with:
            print "DEBUG: ACL for %s exists, verifying role." % share_with
            update_acl = acl
    if update_acl:
        if not update_acl.role.value == role:
            print "DEBUG: ACL Scope: %s ACL Role: %s" % (update_acl.scope.value, update_acl.role.value)
            update_acl.role.value = role
            print "DEBUG: ACL Scope: %s ACL Role: %s" % (update_acl.scope.value, update_acl.role.value)
            new_acl = gdata.docs.data.AclEntry(
                scope=gdata.acl.data.AclScope(value=share_with, type='user'),
                role=gdata.acl.data.AclRole(value=role)
            )
            client.UpdateAclEntry(new_acl, send_notification=False)
        updated = True
    #add new ACL entry with proper role for share_with
    if not updated:
        print "DEBUG: Sharing with %s" % share_with
        acl_entry = gdata.docs.data.AclEntry(
            scope=gdata.acl.data.AclScope(value=share_with, type='user'),
            role=gdata.acl.data.AclRole(value=role))
        client.AddAclEntry(folder, acl_entry, send_notification=False)

def analyze_share_structure(client, conn, folder_entry):
    enrollment = Database.get(Database.execute(conn, Database.enrollment_query_string(where="class_id = '" + folder_entry['class_id'] + "' AND student_id = '" + folder_entry['student_id'] + "'")))
    parent_res_id = ""
    directory_folders = None
    max_level = 0

    structures = retrieve_share_structures()
    new_structures = {}

    for name, structure in structures.iteritems():
        new_structure = {}
        for template, level in structure.iteritems():
            if (level > max_level):
                max_level = level
        for template, level in structure.iteritems():
            folder = ShareTemplate.get(client, conn, template, enrollment)

            if level == 0:
                directory_folders = Folder.list_sub_folders(client, folder['parent_id'])
                parent_res_id = folder['parent_id']
                parent_res_id = create_share_structure(client, folder, level, template, max_level, parent_res_id)
                new_structure[level] = {'folder_id':parent_res_id, 'role':folder['role']}
            elif level != max_level:
                parent_res_id = create_share_structure(client, folder, level, template, max_level, parent_res_id)         
                new_structure[level] = {'folder_id':parent_res_id, 'role':folder['role']}
            else:
                folder_id = create_share_structure(client, folder, level, template, max_level, parent_res_id)
                new_structure[level] = {'folder_id':folder_id, 'role':folder['role']}

        new_structures[name] = OrderedDict(sorted(new_structure.items(), key=lambda d: d[0]))

    return enrollment, new_structures

def create_share_structure(client, folder, level, template, max_level, parent_res_id):
    directory_folders = Folder.list_sub_folders(client, parent_res_id)
    #Make sure the folder isn't the student assignment folder
    if not folder['isassignment']:                  
        #If the folder is already there, store the resource_id and move on
        if folder['folder_name'] in directory_folders:
            print "DEBUG: Folder exists, ", directory_folders[folder['folder_name']]
            return directory_folders[folder['folder_name']]
        #If the folder is not there, create it, store the id, and move on
        else:
            print "DEBUG: Creating new folder", template
            new_folder = create_folder(client, folder['folder_name'], parent_res_id)
            return new_folder.resource_id.text
    else:
        if folder['folder_id'] in directory_folders:
            print "DEBUG: Folder exists, ", folder['folder_id']
            return folder['folder_id']
        else:
            print "DEBUG: Copying assignment folder"
            return Folder.copy(client, folder['folder_id'], parent_res_id)

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

## Testing / Debugging variables ##
## client = Client.create()
## conn = Database.connect()
## folder_entry = {'id':'296', 'class_id':'1771', 'student_id':'66839', 'folder_name':'Andrews, Henry - Assignments', 'folder_id':'folder:0B7AqvGrb_oO8cy1Ydy00LVlCdXc', 'folder_parent':'folder:0B7AqvGrb_oO8UVNJVl80aWNkWXM', 'isactive':1}
##
##
##
##