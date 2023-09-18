from django.urls import path , include

from BackEnd import Teacher_Views
from . import views ,HOD_Views,Staff_Views , Guest_Views
urlpatterns = [
   
    path('',views.login,name='login'),
   
   

    path('profile/',views.profile,name='profile'),
    path('profile/edit',views.editprofile,name='editprofile'),
    path('hod/',HOD_Views.HOD_HOME,name='hod_home'),
    path('hod/download/backup/of/all',HOD_Views.backup_data,name='backup_data'),
    path('hod/contact/views',HOD_Views.contact_views,name='contact_views'),
    path('hod/news/add/',HOD_Views.HOD_News,name='hod_news'),
    path('hod/news/add/save',HOD_Views.HOD_News_add,name='hod_add_news'),
    path('hod/admissions/request',HOD_Views.request_views,name='request_views'),
    path('hod/admissions/<str:student_name>/request',HOD_Views.request_views_student,name='request_views_studnet'),
    path('hod/blogs',HOD_Views.Hod_Blogs,name='hod_blogs'),
    path('hod/blogs/add',HOD_Views.Hod_Blog_add,name='hod_blog_add'),
    path('hod/blogs/delete/<str:slug>',HOD_Views.Hod_Blog_delete,name='hod_blog_delete'),
    path('hod/blogs/add/image',HOD_Views.add_image,name='image_save'),
    
    path('hod/blogs/categories/add',HOD_Views.Hod_Blog_categories_add,name='add_categories'),
    path('hod/blogs/tags_cloud/add',HOD_Views.Hod_Blog_tags_cloud_add,name='add_tags_cloud'),
    
    path('hod/class/list',HOD_Views.Result_C,name='result'),
    path('hod/class/<str:id>/section/list',HOD_Views.Result_C_Section,name='result_c_s'),
    path('hod/class/<str:id>/section/<str:sid>/examsession/list',HOD_Views.Result_EL,name='result_el'),
    path('hod/class/<str:id>/section/<str:sid>/examseession/<str:ied>/result',HOD_Views.Result_C_SectionPStudnet,name='result_c_sps'),
    path('hod/class/<str:id>/section/<str:sid>/examseession/<str:ied>/result/add',HOD_Views.ResultAdd,name='result_add'),
    path('hod/website-front/',HOD_Views.HOD_HOME_fornt,name='hod_home_front'),
    path('hod/website-front/update/',HOD_Views.HOD_HOME_fornt_update,name='hod_home_front_update'),
    path('hod/website-front/edit/<str:id>',HOD_Views.HOD_HOME_fornt_edit,name='hod_home_front_edit'),
   
    path('hod/student/',HOD_Views.Student,name='hod_student'),
    path('hod/student/attendance',HOD_Views.AttendanceView,name='hod_attendance_view_student'),
    path('hod/teacher/',HOD_Views.Teachers,name='hod_teacher'),
    path('hod/staffs/',HOD_Views.STAff,name='hod_staffs'),
    path('hod/staffs/add',HOD_Views.Staff_add,name='hod_staffs_add'),
    path('hod/staffs/edit/<str:id>',HOD_Views.STAff_edit,name='hod_staffs_edit'),
   
    path('hod/staffs/update',HOD_Views.Staff_update,name='hod_staffs_update'),
    path('hod/staffs/detail/<str:id>',HOD_Views.Staff_detail,name='hod_staffs_detail'),
    path('hod/staffs/delete/<str:admin>',HOD_Views.Staff_delete,name='hod_staffs_delete'),
    path('hod/student/add/',HOD_Views.Student_add,name='hod_student_add'),
    path('hod/student/detail/<str:id>',HOD_Views.Student_detail,name='hod_student_detail'),
    path('hod/teacher/detail/<str:id>',HOD_Views.Teacher_detail,name='hod_teacher_detail'),
    path('hod/student/update/',HOD_Views.Student_update,name='hod_student_update'),
    path('hod/teacher/update/',HOD_Views.Teacher_update,name='hod_teacher_update'),
    path('hod/student/delete/<str:admin>',HOD_Views.Student_delete,name='hod_student_delete'),
    path('hod/teacher/delete/<str:admin>',HOD_Views.Teacher_delete,name='hod_teacher_delete'),
    path('hod/student/edit/<str:id>',HOD_Views.Student_edit,name='hod_student_edit'),
    path('hod/teacher/add/',HOD_Views.Teacher_add,name='hod_teacher_add'),
    path('hod/teacher/edit/<str:id>',HOD_Views.Teacher_edit,name='hod_teacher_edit'),
    path('hod/salary/',HOD_Views.salary,name='salary'),
    path('hod/salary/history',HOD_Views.salary_history,name='salary_history'),
    path('hod/salary/pay/<str:id>',HOD_Views.salaryP,name='salary_pay'),
    path('hod/fees/',HOD_Views.fees,name='fees'),
    path('hod/fees/exam/set',HOD_Views.add_exam_fees_for_all_students,name='add_exam_fees_for_all_students'),
    path('hod/fees/history',HOD_Views.fees_history,name='fees_history'),
    path('hod/fees/pay/<str:id>',HOD_Views.fees_Pay,name='fees_pay'),

    # path('hod/fees/month/all',HOD_Views.add_monthly_fees_for_all_students,name='add_monthly_fees_for_all_students'),
    # path('hod/fees/annual/all',HOD_Views.add_annual_fees_for_all_students,name='add_annual_fees_for_all_students'),
    path('hod/fees/exam/all',HOD_Views.add_exam_fees_for_all_students,name='add_exam_fees_for_all_students'),
    path('hod/exams/',HOD_Views.ExamSave,name='hod_exam'),
    path('hod/transprot/',HOD_Views.Transport,name='transport'),
    path('hod/transprot/vehicles/<str:id>/route',HOD_Views.Transport_Route,name='transport_R1'),
    path('hod/transprot/vehicles/<str:id>/route/stops',HOD_Views.Stops,name='stops'),
    path('hod/transprot/vehicles/<str:id>/route/stops/riders/add',HOD_Views.add_rider,name='add_rider'),
    path('hod/transprot/vehicles/<str:id>/route/stops/add',HOD_Views.Stops_add,name='stops_add'),
    path('hod/transprot/vehicles/<str:id>/route/add',HOD_Views.Transport_Route_Ad,name='transport_R1_add'),
    path('hod/transprot/vehicles/add',HOD_Views.Transport_V2,name='transport_v2'),
    path('hod/hostel/',HOD_Views.hostel_,name='hostel'),
    path('hod/hostel/<str:id>/rooms',HOD_Views.hostel_R,name='hostel_r'),
    path('hod/hostel/<str:id>/rooms/hostelers/add',HOD_Views.hostel_R_H,name='hostel_r_h'),
   
    path('hod/hostel/add',HOD_Views.hostel_add,name='hostel_add'),
    path('hod/hostel/<str:id>/add/room',HOD_Views.RooMS_Add,name='room_add'),
    path('hod/exams/add',HOD_Views.ExamAdd,name='exams_add'),
    path('hod/exams/delete/<str:id>',HOD_Views.ExamDelete,name='exams_delete'),
    path('hod/sections/',HOD_Views.sections,name='sections'),
    path('hod/sections/add',HOD_Views.add_sections,name='add_sections'),
    path('hod/sections/save',HOD_Views.save_sections,name='save_section'),
    # path('hod/sections/update',HOD_Views.section_update,name='section_update'),
    # path('hod/sections/edit/<str:id>',HOD_Views.Section_edit,name='section_edit'),
    path('hod/sections/delete/<str:id>',HOD_Views.section_delete,name='section_delete'),
    path('hod/subjects/',HOD_Views.subjects,name='subjects'),
    path('hod/subjects/delete/<str:id>',HOD_Views.subject_delete,name='subject_delete'),
    path('hod/subjects/add',HOD_Views.add_subject,name='add_subjects'),
    path('hod/subjects/save',HOD_Views.save_subject,name='save_subjects'),
    path('hod/time-table/',HOD_Views.Time_Table,name='timetable'),
    path('hod/time-table/add',HOD_Views.Time_Table_add,name='add_timetable'),
    path('hod/meetings/',HOD_Views.Meeting,name='hod_meetings'),
    path('hod/meetings/add',HOD_Views.Meetings_add,name='meetings_add'),
    path('hod/meetings/edit/<str:id>',HOD_Views.Meeting_edit,name='meetings_edit'),
    path('hod/meetings/delete/<str:id>',HOD_Views.Meeting_delete,name='meetings_delete'),
    path('hod/meetings/update/',HOD_Views.Meeting_updade,name='meetings_update'),
    path('hod/events/',HOD_Views.Event,name='hod_events'),
    path('hod/events/add',HOD_Views.Events_add,name='events_add'),
    path('hod/events/edit/<str:id>',HOD_Views.Events_edit,name='events_edit'),
    path('hod/events/delete/<str:id>',HOD_Views.Events_delete,name='events_delete'),
    path('hod/events/update/',HOD_Views.Events_update,name='events_update'),
    path('hod/notification/',HOD_Views.hod_notification,name='hod_notification'),
    path('hod/notification/guest/',HOD_Views.hod_notification_guest,name='hod_notification_guest'),
    path('hod/notification/guest/send_notification',HOD_Views.hod_notification_guest_send,name='hod_notification_guest_send'),
    path('hod/notification/teacher/',HOD_Views.hod_notification_teacher,name='hod_notification_teacher'),
    path('hod/notification/teacher/send_notification',HOD_Views.hod_notification_teacher_send,name='hod_notification_teacher_send'),
    path('hod/notification/staff',HOD_Views.hod_notification_staff,name='hod_notification_staff'),
    path('hod/notification/staff/send_notification',HOD_Views.hod_notification_staff_send,name='hod_notification_staff_send'),
    path('hod/leave/views',HOD_Views.hod_leave_views,name='hod_leave_views'),
    path('hod/leave/views/staff/approve/<str:status>',HOD_Views.hod_leave_views_staff_approve,name='hod_leave_view_staff_approve'),
    path('hod/leave/views/staff/disapprove/<str:status>',HOD_Views.hod_leave_views_staff_disapprove,name='hod_leave_view_staff_disapprove'),
    path('hod/leave/views/student/approve/<str:status>',HOD_Views.hod_leave_views_student_approve,name='hod_leave_view_student_approve'),
    path('hod/leave/views/student/disapprove/<str:status>',HOD_Views.hod_leave_views_student_disapprove,name='hod_leave_view_student_disapprove'),
    path('hod/leave/views/teacher/approve/<str:status>',HOD_Views.hod_leave_views_teacher_approve,name='hod_leave_view_teacher_approve'),
    path('hod/leave/views/teacher/disapprove/<str:status>',HOD_Views.hod_leave_views_teacher_disapprove,name='hod_leave_view_teacher_disapprove'),
    path('hod/feedback',HOD_Views.hod_feedback,name='hod_feedback'),
    path('hod/feedback/staff/reply',HOD_Views.hod_feedback_staff_reply,name='hod_feedback_staff_reply'),
    path('hod/feedback/guest/reply',HOD_Views.hod_feedback_guest_reply,name='hod_feedback_guest_reply'),
    path('hod/feedback/teacher/reply',HOD_Views.hod_feedback_teacher_reply,name='hod_feedback_teacher_reply'),




    # Staff urls
    path('staff/' ,Staff_Views.STAFF_HOME,name='staff_home'),
    path('staff/view/salary' ,Staff_Views.view_salary,name='view_salary_s'),
  
    path('staff/meetings' ,Staff_Views.STAFF_Mettings,name='staff_mettings'),
    

    path('staff/notification' ,Staff_Views.STAFF_Notification,name='staff_notification'),
    path('staff/notification/seen/<str:status>' ,Staff_Views.STAFF_Notification_seen,name='staff_notification_seen'),
    path('staff/apply_leave' ,Staff_Views.STAFF_Apply_leave,name='staff_apply_leave'),
    path('staff/apply_leave/send' ,Staff_Views.STAFF_Apply_leave_send,name='staff_apply_leave_send'),
    path('staff/feedback/send' ,Staff_Views.STAFF_feedback_send,name='staff_feedback_send'),
    path('staff/feedback' ,Staff_Views.STAFF_feedback,name='staff_feedback'),
    path('staff/feedback/detail/<str:status>' ,Staff_Views.STAFF_feedback_detail,name='staff_feedback_detail'),
   
    path('staff/student/detail/<str:id>',Staff_Views.Student_detail,name='staff_student_detail'),
    
    
    # Teacher urls
    path('teacher/' ,Teacher_Views.T_HOME,name='t_home'),
    path('teacher/view/salarys' ,Teacher_Views.view_salary,name='view_salary_t'),
    path('teacher/blog/add' ,Teacher_Views.T_add_blog,name='t_blog_add'),
    path('teacher/blog/image/add' ,Teacher_Views.T_add_Image_blog,name='t_blogimage_add'),

    path('teacher/exams' ,Teacher_Views.exam_t,name='exams_t'),
    path('teacher/meetings' ,Teacher_Views.T_Mettings,name='t_mettings'),
    path('teacher/time_table' ,Teacher_Views.T_timetable,name='t_timetable'),

    path('teacher/notification' ,Teacher_Views.T_Notification,name='teacher_notification'),
    path('teacher/notification/seen/<str:status>' ,Teacher_Views.T_Notification_seen,name='t_notification_seen'),
    path('teacher/apply_leave' ,Teacher_Views.T_Apply_leave,name='teacher_apply_leave'),
    path('teacher/apply_leave/send' ,Teacher_Views.T_Apply_leave_send,name='t_apply_leave_send'),
    path('teacher/feedback/send' ,Teacher_Views.T_feedback_send,name='t_feedback_send'),
    path('teacher/feedback' ,Teacher_Views.T_feedback,name='teacher_feedback'),
    path('teacher/feedback/detail/<str:status>' ,Teacher_Views.T_feedback_detail,name='t_feedback_detail'),
    path('teacher/take/attandance' ,Teacher_Views.take_attandance,name='teacher_take_attandance'),
    path('teacher/take/attandance/send' ,Teacher_Views.take_attendance_send,name='t_take_attandance_send'),
    path('teacher/student/detail/<str:id>',Teacher_Views.Student_detail,name='t_student_detail'),
    
    



    # guest_ urls
    path('guest/' , Guest_Views.Index ,name='guest_home'),
    path('guest/list/exam' , Guest_Views.exam_guest ,name='guest_exam'),
    path('guest/my_fees' , Guest_Views.fees ,name='my_fees'),
    path('guest/my_result' , Guest_Views.view_result ,name='view_result'),


    path('guest/blog/add' , Guest_Views.blog_add ,name='guest_add_blog'),
    path('guest/blog/image/add' , Guest_Views.Image_blog_add ,name='guest_add_blogimage'),

   
    path('guest/time_table' ,Guest_Views.Student_timetable,name='guest_timetable'),
    path('guest/meetings' , Guest_Views.Guest_Mettings ,name='guest_mettings'),
    path('guest/events' , Guest_Views.Guest_Events ,name='guest_events'),
    path('guest/notification/' , Guest_Views.Guest_notification ,name='guest_Notification'),
    path('guest/notification/seen/<str:status>' , Guest_Views.Guest_Notification_seen ,name='guest_notification_seen'),
    path('guest/apply_leave' ,Guest_Views.Guest_Apply_leave,name='guest_apply_leave'),
    path('guest/apply_leave/send' ,Guest_Views.Guest_Apply_leave_send,name='guest_apply_leave_send'),
    path('guest/feedback/send' ,Guest_Views.Guest__Feedback_send,name='guest_feedback_send'),
    path('guest/feedback' ,Guest_Views.Guest__Feedback,name='guest_feedback'),
    path('guest/feedback/detail/<str:status>' ,Guest_Views.Guest_feedback_detail,name='guest_feedback_detail'),
    path('guest/views/attendance' ,Guest_Views.Guest_Views_Attendance,name='guest_views_attendance'),
    

]