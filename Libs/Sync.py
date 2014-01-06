#!/usr/bin/python

_author_ = 'mgeorge@vlacs.org (Mike George)'

from Libs import Database
from Libs import Utilities

def not_synced(enrollment, database_contents):
    for entry in database_contents:
        if (gen_title(enrollment, "s") == entry['folder_name'] and 
            int(enrollment.course.id)  == int(entry['course_id'])):
            return False
    return True

def course_needs_renaming(conn, enrollment):
    qs = Database.construct_query_string('vlacs_class_folders_structure', 
                                        {'folder_name' : 
                                            {'value' : Utilities.gen_title(enrollment, "c"),
                                             'type' : 's'}})
    needs_renaming = Database.get(Database.execute(conn, qs))
    if len(needs_renaming) > 0:
        return False
    enrollment.folder_id = needs_renaming['folder_id']
    enrollment.folder_name = Utilites.gen_title(enrollment, "c")
    return True

def student_needs_renaming(enrollment, database_contents):
    for entry in database_contents:
        if (enrollment.student.id == entry['student_id'] and
            Utilities.gen_title(enrollment, "s") != entry['folder_name']):
            enrollment.folder_id = entry['folder_id']
            enrollment.folder_name = entry['folder_name']
            return True
    return False

def should_archive(enrollment, database_contents):
    for entry in database_contents:
        if (gen_title(enrollment, "s") == entry['folder_name'] and 
            int(enrollment.course.id)  == int(entry['course_id']) and
            entry['isactive']          == "0"):
        return True
    return False

def not_exists_in_enrollments(entry, enrollments):
    dc_folder_name = deconstruct_title(entry['folder_name'], "s")

    for enrollment in enrollments:
        if(enrollment.course.id          == entry['course_id'] and
            enrollment.student.id        == entry['student_id'] and
            enrollment.student.firstname == dc_folder_name['student_firstname'] and
            enrollment.student.lastname  == dc_folder_name['student_lastname']):
        return False
    return True