from django.urls import path, re_path
from .views import CreateCourseView, CourseListView, CourseEnrollView, CourseUnenrollView
from . import views
import re

app_name = 'course'

urlpatterns = [
    path('create/', CreateCourseView.as_view(), name='create_course'),
    path('list/', CourseListView.as_view(), name='course_list'),
    path('enroll/', CourseEnrollView.as_view(), name='course_enroll'),
    path('unenroll/', CourseUnenrollView.as_view(), name='course_unenroll'),
    re_path(r'^(?P<course_id>[\w-]+)/$', views.course_detail_view, name='detail'),
]
