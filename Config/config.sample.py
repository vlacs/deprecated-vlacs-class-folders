#!/usr/bin/python
#Sample config for vlacs-class-folders
#You must rename this file to config.py and insert your own data

__author__ = 'mgeorge@vlacs.org'

#Master google drive account username and password
USERNAME = ""
PASSWORD = ""

#Root Folder Names
ROOT_CLASS_FOLDER = ""
TEACHER_SHARE_FOLDER = ""
STUDENT_SHARE_FOLDER = ""

#APP NAME
APP_NAME = "vlacs-class-folders"

#Postgres Database Connection Information
DATABASE = {
    'host' : '',
    'database' : '',
    'user' : '',
    'password' : '',
}

## SHARE STRUCTURES ##
## Set up so teachers and students can each use two
## different share structures to access their documents
## Accepted Template Variables:
##   {{TEACHER_ROOT}} Root Teacher Share Folder
##   {{STUDENT_ROOT}} Root Student Share Folder
##   {{STUDENTS}} Folder called Students
##   {{COURSES}} Folder called Courses
##   {{STUDENT_NAME}} Folder with student name (Last Name, First Name)
##   {{COURSE_NAME}} Folder with Master Course Name
##   {{CLASSROOM}} Folder with Classroom ID and Version
##   {{CLASS_FILES}} Teacher writable Student accessable folder for class files
##   {{STUDENT_ASSIGNMENTS}} Students' assignment folder
## Each folder level should be seperated with a /
## "{{TEACHER_ROOT}}/{{STUDENTS}}/{{STUDENT_NAME}}/{{COURSE_NAME}}/{{STUDENT_ASSIGNMENTS}}"
## If you'd like two or more types of folders at the same level:
## "{{TEACHER_ROOT}}/{{COURSES}}/{{COURSE_NAME}}/{{CLASSROOM}}/{{CLASS_FILES}}{{STUDENT_ASSIGNMENTS}}"
######################

#Main Teacher Share Structure
TEACHER_SHARE_STRUCTURE = "{{TEACHER_ROOT}}/{{STUDENTS}}/{{STUDENT_NAME}}/{{COURSE_NAME}}/{{STUDENT_ASSIGNMENTS}}"
#Optional Alternate Share Structure
ALT_TEACHER_SHARE_STRUCTURE = "{{TEACHER_ROOT}}/{{COURSES}}/{{COURSE_NAME}}/{{CLASSROOM}}/{{CLASS_FILES}}{{STUDENT_ASSIGNMENTS}}"

#Main Student Share Structure
STUDENT_SHARE_STRUCTURE = "{{STUDENT_ROOT}}/{{COURSE_NAME}}/{{CLASS_FILES}}{{STUDENT_ASSIGNMENTS}}"
#Optional Alternate Share Structure
ALT_STUDENT_SHARE_STRUCTURE = ""
