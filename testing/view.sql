SELECT mmc.master_course_idstr as master_id,
       mce.classroom_idstr as class_id,
       mmc.name as course_name,
       mce.sis_user_idstr as student_id,
       msu.firstname as student_firstname,
       msu.lastname as student_lastname
       FROM
           mdl_sis_user msu LEFT OUTER JOIN mdl_classroom_enrolment mce on (mce.sis_user_idstr = msu.sis_user_idstr)
       	LEFT OUTER JOIN mdl_classroom mc on (mc.classroom_idstr = mce.classroom_idstr)
            	    LEFT OUTER JOIN mdl_master_course mmc on (mmc.master_course_idstr = mc.master_course_idstr)
       WHERE msu.privilege = 'STUDENT' AND mc.status = 'ACTIVE' AND mce.status_idstr = 'ACTIVE'
       LIMIT(20);
