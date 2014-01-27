#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

from contextlib import contextmanager

from Objects.Enrollment import Enrollment

import string, sys

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
    enrollment = Enrollment()
    if type == "s":
        student_lastname = title.split(',')[0]
        student_firstname = title.split(',')[1].split('-')[0].strip()

        enrollment.student.lastname = student_lastname
        enrollment.student.firstname = student_firstname
    else:
        teacher_lastname = title.split('-')[1].strip().split(" ")[1]
        teacher_firstname = title.split('-')[1].strip().split(" ")[0]
        course_version = title.split('-')[2].strip()
        course_name = title.split('-')[0].strip()
        course_id = title.split('-')[3].strip()

        enrollment.teacher.lastname = teacher_lastname
        enrollment.teacher.firstname = teacher_firstname
        enrollment.course.version = course_version
        enrollment.course.name = course_name
        enrollment.course.id = course_id

    return enrollment

def gen_title(enrollment, type):
    title = ""
    if type == "s":
        title += clean_name(enrollment.student.lastname)
        title += ", "
        title += clean_name(enrollment.student.firstname)
        title += " - Assignments"
    else:
        title += enrollment.course.name 
        title += " - "
        title += clean_name(enrollment.teacher.firstname)
        title += " "
        title += clean_name(enrollment.teacher.lastname)
        title += " - "
        title += enrollment.course.version
        title += " - "
        title += enrollment.course.id
    return title

def remove_from_list(l_remove, l_from):
    for v in l_remove:
        l_from.remove(v)
    return l_from