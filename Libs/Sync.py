_author_ = 'mgeorge@vlacs.org (Mike George)'

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

def not_exists_in_enrollments(entry, enrollments):
    dc_folder_name = deconstruct_title(entry['folder_name'], "s")

    for enrollment in enrollments:
        if(enrollment['class_id'] == entry['class_id'] and
            enrollment['student_id'] == entry['student_id'] and
            enrollment['student_firstname'] == dc_folder_name['student_firstname'] and
            enrollment['student_lastname'] == dc_folder_name['student_lastname']):
        return False
    return True