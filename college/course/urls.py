import re
from course import views
from course.views import CreateCourseView, CourseListView, CourseEnrollView, CourseUnenrollView, StripePaymentView
from django.urls import path, re_path

app_name = 'course'

urlpatterns = [
    path('create/', CreateCourseView.as_view(), name='create_course'),
    path('list/', CourseListView.as_view(), name='course_list'),
    path('enroll/', CourseEnrollView.as_view(), name='course_enroll'),
    path('unenroll/', CourseUnenrollView.as_view(), name='course_unenroll'),
    path("initiate-payment/", views.initiate_razorpay_payment, name="initiate_razorpay_payment"),
    path('initiate-payment/', views.initiate_cashfree_payment, name='initiate_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('stripe_payment/', StripePaymentView.as_view(), name='stripe_payment'),
    re_path(r'^(?P<course_id>[\w-]+)/$', views.course_detail_view, name='detail'),

]