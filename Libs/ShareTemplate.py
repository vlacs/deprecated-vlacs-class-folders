__author__ = 'mgeorge@vlacs.org (Mike George)'

from Config import config
from Libs import Utilities

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

get(template, enrollment=None):
	parsed_template = {'folder_name': "", 'role': {'teacher': "", 'student': ""}}

	if template == "{{TEACHER_ROOT}}":
		parsed_template['folder_name'] = config.TEACHER_SHARE_FOLDER
		parsed_template['role']['teacher'] = 'reader'
		parsed_template['role']['student'] = 'reader'
	elif template == "{{STUDENT_ROOT}}":
		parsed_template['folder_name'] = config.STUDENT_SHARE_FOLDER
		parsed_template['role']['teacher'] = 'reader'
		parsed_template['role']['student'] = 'reader'
	elif template == "{{STUDENTS}}":
		parsed_template['folder_name'] = "Students"
		parsed_template['role']['teacher'] = 'reader'
		parsed_template['role']['student'] = 'reader'
	elif template == "{{COURSES}}":
		parsed_template['folder_name'] = "Courses"
		parsed_template['role']['teacher'] = 'reader'
		parsed_template['role']['student'] = 'reader'
	elif template == "{{STUDENT_NAME}}":
		parsed_template['folder_name'] = "%s, %s" % (enrollment['student_lastname'], enrollment['student_firstname'])
		parsed_template['role']['teacher'] = 'reader'
		parsed_template['role']['student'] = 'reader'
	elif template == "{{COURSE_NAME}}":
		parsed_template['folder_name'] = "%s" % (enrollment['course_name'])
		parsed_template['role']['teacher'] = 'reader'
		parsed_template['role']['student'] = 'reader'
	elif template == "{{CLASSROOM}}":
		parsed_template['folder_name'] = "%s - %s" % (enrollment['class_id'], Utilities.course_version(enrollment['course_full_name']))
		parsed_template['role']['teacher'] = 'reader'
		parsed_template['role']['student'] = 'reader'
	elif template == "{{CLASS_FILES}}":
		parsed_template['folder_name'] = "Class Files"
		parsed_template['role']['teacher'] = 'writer'
		parsed_template['role']['student'] = 'reader'
	elif template == "{{STUDENT_ASSIGNMENTS}}":
		parsed_template['folder_name'] = Utilities.gen_title(enrollment, "s")
		parsed_template['role']['teacher'] = 'writer'
		parsed_template['role']['student'] = 'writer'

	return parsed_template