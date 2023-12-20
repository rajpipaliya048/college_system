from college import views
from course.views import CourseListView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from users import views as userviews
from users.views import Actions, SignupView, LoginView, LogoutView, EditProfileView, SendEmail, UpdateUserFromCsv, CsvReport, PaymentSelectionView

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
    path('update/<uidb64>/<token>/', userviews.update_email, name='update'),
    path('email_updated/', userviews.email_updated, name='email_updated'),
    path('update-skills/', userviews.update_skills, name='update_skills'),
    path('update-users-from-csv/', UpdateUserFromCsv.as_view(), name='update_users_from_csv'),
    path('send-email/', SendEmail.as_view(), name='send_email'),
    path('csv-report/', CsvReport.as_view(), name='csv_report'),
    path('actions/', Actions.as_view(), name='actions'),
    path('payment-selection/', PaymentSelectionView.as_view(), name='payment_selection'),
    # path('api/', include('course.urls')),



]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
