from django.conf.urls import url
from . import views
app_name= 'login'

urlpatterns = [
    #/dashboard/
    #url(r'^$', views.dashview, name='dashview'),
    url(r'^$', views.common, name='common'),
    url(r'^student_login/$', views.student_login, name='student_login'),
    url(r'^student_detail/$', views.student_detail, name='student_detail'),
    url(r'^academics/$',views.academic_detail, name='academic_detail'),
    url(r'^complaint_user/$', views.complaint_user, name='complaint_user'),
    url(r'^teacher_profile/$', views.teacher_profile, name='teacher_profile'),
    url(r'^add_marks/$', views.add_marks, name='add_marks'),
    url(r'^modify_marks/$', views.modify_marks, name='modify_marks'),
    url(r'^send_notice/$', views.send_notice, name='send_notice'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^staff_login/$', views.staff_login, name='staff_login'),
    url(r'^admin_login/$', views.admin_login, name='admin_login'),
    url(r'^register_student/$', views.register_student, name='register_student'),
    url(r'^modify_student/$', views.modify_student, name='modify_student'),
    url(r'^modify_teacher/$', views.modify_teacher, name='modify_teacher'),
    url(r'^deregister/$', views.deregister, name='deregister'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_teacher/$', views.register_teacher, name='register_teacher'),
    url(r'^register_caretaker/$', views.register_caretaker, name='register_caretaker'),
    url(r'^register_driver/$', views.register_driver, name='register_driver'),
    url(r'^add_news/$', views.add_news, name='add_news'),
    url(r'^view_complaint/$', views.view_complaint, name='view_complaint'),
    url(r'^update_fees/$', views.update_fees, name='update_fees'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^admin_password/$', views.admin_password, name='admin_password'),
    url(r'^teacher_password/$', views.teacher_password, name='teacher_password'),
   
    
]
