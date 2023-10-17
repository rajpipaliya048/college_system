from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_course, name='create_course'),
    path('list/', views.course_list, name='course_list'),
    path('enroll/', views.course_enroll, name='course_enroll'),

]
