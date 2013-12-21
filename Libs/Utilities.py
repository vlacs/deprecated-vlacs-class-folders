#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from contextlib import contextmanager
import string

def clean_name(name):
    clean = name
    clean = string.capitalize(clean)

    return clean

def clean_title(title):
    clean = title
    clean = string.replace(clean, "'", "''")

    return clean

def course_version(course_full_name):
    course_version = course_full_name
    course_version = course_version.split("-")
    course_version = course_version[1].split("_")

    return course_version[0]

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

def fix_nulls(dict):
    for k, v in dict.items():
        if v == None:
            dict[k] = k + " - NULL"
    return True

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

@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass

@contextmanager
def redirect_stdout(fileobj):
    oldstdout = sys.stdout
    sys.stdout = fileobj
    try:
        yield fileobj
    finally:
        sys.stdout = oldstdout

def remove_duplicates(list):
    seen = set()
    result = []

    for d in list:
        i = d.copy()
        i = tuple(i.items())
        if i not in seen:
            result.append(d)
            seen.add(i)

    return result

##test remove_duplicates
## list = [{"key":"value", "hello":"there"},{"key":"value", "hello":"different"},{"key":"value", "hello":"there"}]
##
##
##
########################