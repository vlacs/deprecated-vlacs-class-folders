__author__ = 'mgeorge@vlacs.org (Mike George)'

from Config import config
from Libs import Database
from Libs import Folder
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

def get(client, conn, template, enrollment=None):
	parsed_template = {'folder_name': "", 'role': {'teacher': "", 'student': ""}}

	# These template variables rely on external systems, we shouldn't generate them
	# each time the function is called.
	if template == "{{TEACHER_ROOT}}":
		root_folders = Folder.list_sub_folders(client, "root")
		parsed_template['folder_id'] = root_folders[config.TEACHER_SHARE_FOLDER]
		parsed_template['role']['teacher'] = 'reader'
		parsed_template['role']['student'] = 'reader'
		parsed_template['isassignment'] = False
	elif template == "{{STUDENT_ROOT}}":
		root_folders = Folder.list_sub_folders(client, "root")
		parsed_template['folder_id'] = root_folders[config.STUDENT_SHARE_FOLDER]
		parsed_template['role']['teacher'] = 'reader'
		parsed_template['role']['student'] = 'reader'
		parsed_template['isassignment'] = False
	elif template == "{{STUDENT_ASSIGNMENTS}}":
		folder_id = Database.get(Database.execute(conn, Database.structure_get_folder_id_string(Utilities.gen_title(enrollment, "s"), enrollment['class_id'], enrollment['student_id'])))
		folder_id = folder_id['folder_id']
		parsed_template['folder_id'] = folder_id
		parsed_template['role']['teacher'] = 'writer'
		parsed_template['role']['student'] = 'writer'
		parsed_template['isassignment'] = True
	else:
		template_variables = {
			"{{CLASS_FILES}}" : {
					 'folder_name' : "Class Files",
					        'role' : {
										'teacher' : 'writer',
										'student' : 'reader',
									},
					'isassignment' : False
			},
			"{{CLASSROOM}}" : {
					 'folder_name' : "%s (%s - %s)" % (enrollment['course_name'], enrollment['class_id'], Utilities.course_version(enrollment['course_full_name'])),
					        'role' : {
										'teacher' : 'reader',
										'student' : 'reader',
									},
					'isassignment' : False
			},
			"{{COURSE_NAME}}" : {
					 'folder_name' : enrollment['course_name'],
					        'role' : {
										'teacher' : 'reader',
										'student' : 'reader',
									},
					'isassignment' : False
			},
			"{{COURSES}}" : {
					 'folder_name' : "Courses",
					        'role' : {
										'teacher' : 'reader',
										'student' : 'reader',
									},
					'isassignment' : False
			},
			"{{STUDENT_NAME}}" : {
					 'folder_name' : "%s, %s" % (enrollment['student_lastname'], enrollment['student_firstname']),
					        'role' : {
										'teacher' : 'reader',
										'student' : 'reader',
									},
					'isassignment' : False
			},
			"{{STUDENTS}}" : {
					 'folder_name' : "Students",
					        'role' : {
										'teacher' : 'reader',
										'student' : 'reader',
									},
					'isassignment' : False
			},
		}
		parsed_template = template_variables[template]

	return parsed_template