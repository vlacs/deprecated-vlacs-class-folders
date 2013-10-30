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