#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import string

def gen_title(enrollment, type):
    title = ""
    if type == "s":
        title += clean_name(enrollment['student_lastname'])
        title += ", "
        title += clean_name(enrollment['student_firstname'])
        title += " - Assignments"
    else:
        title += enrollment['course_name'] 
        title += " - "
        title += clean_name(enrollment['teacher_firstname'])
        title += " "
        title += clean_name(enrollment['teacher_lastname'])
        title += " - "
        title += course_version(enrollment['course_full_name'])
        title += " - "
        title += enrollment['class_id']
    return title

def deconstruct_title(title, type):
    enrollment = {}
    if type == "s":
        student_lastname = title.split(',')[0]
        student_firstname = title.split(',')[1].split('-')[0].strip()

        enrollment['student_lastname'] = student_lastname
        enrollment['student_firstname'] = student_firstname
    else:
        teacher_lastname = title.split('-')[1].strip().split(" ")[1]
        teacher_firstname = title.split('-')[1].strip().split(" ")[0]
        course_version = title.split('-')[2].strip()
        course_name = title.split('-')[0].strip()
        class_id = title.split('-')[3].strip()

        enrollment['teacher_lastname'] = teacher_lastname
        enrollment['teacher_firstname'] = teacher_firstname
        enrollment['course_version'] = course_version
        enrollment['course_name'] = course_name
        enrollment['class_id'] = class_id

    return enrollment

def clean_title(title):
    clean = title
    clean = string.replace(clean, "'", "''")

    return clean

def clean_name(name):
    clean = name
    clean = string.capitalize(clean)

    return clean

def course_version(course_full_name):
    course_version = course_full_name
    course_version = course_version.split("-")
    course_version = course_version[1].split("_")

    return course_version[0]

def fix_nulls(dict):
    for k, v in dict.items():
        if v == None:
            dict[k] = k + " - NULL"
    return True

def not_synced(enrollment, database_contents):
    for entry in database_contents:
        if (gen_title(enrollment, "s") == entry['folder_name'] and 
            int(enrollment['class_id']) == int(entry['class_id'])):
            return False
    return True

def student_needs_renaming(enrollment, database_contents):
    for entry in database_contents:
        if (enrollment['student_id'] == entry['student_id'] and
            Utilities.gen_title(enrollment, "s") != database_contents['folder_name']):
            return True
    return False

def class_folder_needs_renaming(database_folder, enrollments_folders):
    for folder in enrollments_folders:
        if database_folder['class_id'] == folder['class_id']:
            df = deconstruct_title(database_folder['folder_name'], "c")
            if (folder['teacher_firstname'] != df['teacher_firstname'] and
                folder['teacher_lastname'] != df['teacher_lastname']):
                return True
    return False

def should_archive(enrollment, database_contents):
    for entry in database_contents:
        if (gen_title(enrollment, "s") == entry['folder_name'] and 
            int(enrollment['class_id']) == int(entry['class_id']) and
            entry['isactive'] == "0"):
        return True
    return False
