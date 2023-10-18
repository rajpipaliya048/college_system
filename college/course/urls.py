from django.urls import path
from .views import CreateCourseView, CourseListView, CourseEnrollView, CourseUnenrollView

urlpatterns = [
    path('create/', CreateCourseView.as_view(), name='create_course'),
    path('list/', CourseListView.as_view(), name='course_list'),
    path('enroll/', CourseEnrollView.as_view(), name='course_enroll'),
    path('unenroll/', CourseUnenrollView.as_view(), name='course_unenroll')
]
