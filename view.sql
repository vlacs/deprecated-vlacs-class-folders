CREATE OR REPLACE VIEW view_vlacs_class_folders AS
SELECT mmc.master_course_idstr AS master_id,
	   mce.classroom_idstr AS class_id,
	   mc.name AS course_full_name,
	   mmc.name AS course_name,
	   mce.sis_user_idstr AS student_id,
	   msu.firstname AS student_firstname,
	   msu.lastname AS student_lastname,
	   msu.email AS student_email,
	   tsu.sis_user_idstr AS teacher_id,
	   tsu.firstname AS teacher_firstname,
	   tsu.lastname AS teacher_lastname,
	   tsu.email AS teacher_email
	   FROM mdl_classroom_enrolment mce 
	   JOIN mdl_sis_user msu on msu.sis_user_idstr = mce.sis_user_idstr
	   JOIN mdl_classroom mc on mc.classroom_idstr = mce.classroom_idstr
	   JOIN mdl_master_course mmc on mmc.master_course_idstr = mc.master_course_idstr
	   LEFT JOIN mdl_sis_user tsu on mc.sis_user_idstr = tsu.sis_user_idstr
	   WHERE msu.privilege = 'STUDENT' AND mc.status = 'ACTIVE' AND mce.status_idstr = 'ACTIVE'
	   ORDER BY mmc.master_course_idstr, mc.classroom_idstr;
