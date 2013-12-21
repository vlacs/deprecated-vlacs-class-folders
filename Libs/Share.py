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

def ShareFolder():
    #Create the share structures and then share and modify permissions
    #for student and teacher.
    pass

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
    ##    share_roles = [{"folder:folder_id":{"teacher":"writer", "student":"reader"}},]
    ##
    share_roles = []

    for structure in created_structures.iteritems():
        for folder in structure.iteritems():
            temp_dict[folder['folder_id']] = folder['roles']
            share_roles.append(temp_dict)
    share_roles = Utilities.remove_duplicates(share_roles)

    return share_roles


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
    except (gdata.client.RequestError):
        # Catch the request error and retry up to three times
        # Sometimes we recieve a random 500 error and a retry
        # does the trick
        if try_count > 2:
            sys.exit("ERROR: There seems to be a problem sharing...")
        else:
            try_count += 1
            share(client, folder_id, share_with, role, try_count)