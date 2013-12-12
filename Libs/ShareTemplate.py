__author__ = 'mgeorge@vlacs.org (Mike George)'

from Config import config
from Libs import Database
from Libs import Folder
from Libs import Utilities

## Accepted Template Variables:
##   {{CLASS_FILES}} Teacher writable Student accessable folder for class files
##	 {{CLASSROOM}} Folder with Classroom ID and Version
##   {{COURSE_NAME}} Folder with Master Course Name
##   {{COURSES}} Folder called Courses
##   {{STUDENT_ASSIGNMENTS}} Students' assignment folder
##   {{STUDENT_NAME}} Folder with student name (Last Name, First Name)
##   {{STUDENT_ROOT}} Root Student Share Folder
##   {{STUDENTS}} Folder called Students
##   {{TEACHER_ROOT}} Root Teacher Share Folder

def get(client, conn, template, enrollment=None):
	parsed_template = {'folder_name': "", 'role': {'teacher': "", 'student': ""}}

	template_variables = {
			"{{CLASS_FILES}}" : {
					 'folder_name' : "Class Files (%s)" % (enrollment['class_id']),
					        'role' : {
										'teacher' : 'writer',
										'student' : 'reader',
									},
					'copy' : True
			},
			"{{CLASSROOM}}" : {
					 'folder_name' : "%s (%s - %s)" % (enrollment['course_name'], enrollment['class_id'], Utilities.course_version(enrollment['course_full_name'])),
					        'role' : {
										'teacher' : 'reader',
										'student' : 'reader',
									},
					'copy' : False
			},
			"{{COURSE_NAME}}" : {
					 'folder_name' : enrollment['course_name'],
					        'role' : {
										'teacher' : 'reader',
										'student' : 'reader',
									},
					'copy' : False
			},
			"{{COURSES}}" : {
					 'folder_name' : "Courses",
					        'role' : {
										'teacher' : 'reader',
										'student' : 'reader',
									},
					'copy' : False
			},
			"{{STUDENT_ASSIGNMENTS}}" : {
					 'folder_id'   : "",
					 'folder_name' : "",
					        'role' : {
										'teacher' : 'writer',
										'student' : 'writer',
									},
					'copy' : True
			},
			"{{STUDENT_NAME}}" : {
					 'folder_name' : "%s, %s" % (enrollment['student_lastname'], enrollment['student_firstname']),
					        'role' : {
										'teacher' : 'reader',
										'student' : 'none',
									},
					'copy' : False
			},
			"{{STUDENT_ROOT}}" : {
					 'folder_name' : "",
					 'parent_id'   : "",
					        'role' : {
										'teacher' : 'none',
										'student' : 'reader',
									},
					'copy' : False
			},
			"{{STUDENTS}}" : {
					 'folder_name' : "Students",
					        'role' : {
										'teacher' : 'reader',
										'student' : 'none',
									},
					'copy' : False
			},
			"{{TEACHER_ROOT}}" : {
					 'folder_name' : "",
					 'parent_id'   : "",
					        'role' : {
										'teacher' : 'reader',
										'student' : 'none',
									},
					'copy' : False
			},
		}

	# These template variables rely on external systems, we shouldn't generate them
	# each time the function is called.
	if template == "{{TEACHER_ROOT}}":
		root_folders = Folder.list_sub_folders(client, "root")
		template_variables[template]['parent_id'] = root_folders[config.TEACHER_SHARE_FOLDER]
		template_variables[template]['folder_name'] = config.TEACHER_SHARE_FOLDER + " (%s)" % (enrollment['teacher_id'])
	elif template == "{{STUDENT_ROOT}}":
		root_folders = Folder.list_sub_folders(client, "root")
		template_variables[template]['parent_id'] = root_folders[config.STUDENT_SHARE_FOLDER]
		template_variables[template]['folder_name'] = config.STUDENT_SHARE_FOLDER + " (%s)" % (enrollment['student_id'])
	elif template == "{{STUDENT_ASSIGNMENTS}}":
		folder_id = Database.get(Database.execute(conn, Database.structure_get_folder_id_string(Utilities.gen_title(enrollment, "s"), enrollment['class_id'], enrollment['student_id'])))
		folder_id = folder_id['folder_id']
		template_variables[template]['folder_id'] = folder_id
		template_variables[template]['folder_name'] = "%s, %s - Assignments" % (enrollment['student_lastname'], enrollment['student_firstname'])
		
	parsed_template = template_variables[template]

	return parsed_template