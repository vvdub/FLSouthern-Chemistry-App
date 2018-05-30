from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout
from django.conf.urls import include

urlpatterns = [
   url(r'^$', views.home),
   url(r'^login/$', login, {'template_name': 'accounts/login.html'}),
   url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}),
   url(r'^register/$', views.register, name='register'),
   url(r'^profile/$', views.profile, name='profile'),
   url(r'^course/$', views.course, name='course'),
   url(r'^student/$', views.student, name='student'),
   url(r'^all-courses/$', views.course_list, name='course_list'),
   url(r'^all-courses/(?P<id>\d+)$', views.info, name='info'),
   url(r'^grade/$', views.grade, name='grade'),
   url(r'^all-students/$', views.student_list, name='student_list'),
   url(r'^all-students/(?P<id>\d+)$', views.student_info, name='student_info'),
]