from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users.views import SignupView, LoginView, LogoutView, EditProfileView
from django.conf.urls.static import static
from django.conf import settings
from . import views
from course.views import CourseListView
from users import views as userviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CourseListView.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('profile/', userviews.user_profile, name = 'profile'),
    path('update_profile/', EditProfileView.as_view(), name = 'update_profile'),
    path('course/', include('course.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('account_activation_sent/', userviews.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', userviews.activate, name='activate'),
    path('account_activation_complete/', userviews.account_activation_complete, name='account_activation_complete'),
    path('email_update_sent/', userviews.email_update_sent, name='email_update_sent'),
    path('update/<uidb64>/<token>/', userviews.update, name='update'),
    path('email_updated/', userviews.email_updated, name='email_updated'),
    path('update-skills/', userviews.update_skills, name='update_skills'),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
