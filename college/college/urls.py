from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users import views as user_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', user_views.login_view, name = 'login'),
    path('signup/', user_views.signup_view, name = 'signup'),
    path('logout/', user_views.logout_view, name = 'logout'),
]


urlpatterns += staticfiles_urlpatterns()

