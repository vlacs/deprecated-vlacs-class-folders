SELECT mmc.master_course_idstr as master_id,
       mc.classroom_idstr as class_id,
       mmc.name as course_name,
       mc.sis_user_idstr as teacher_id,
       msu.firstname as teacher_firstname,
       msu.lastname as teacher_lastname
       FROM
           mdl_classroom mc LEFT OUTER JOIN mdl_master_course mmc on (mmc.master_course_idstr = mc.master_course_idstr)
               LEFT OUTER JOIN mdl_sis_user msu on (msu.sis_user_idstr = mc.sis_user_idstr)
       WHERE mc.status = 'ACTIVE'
       LIMIT(20);
