from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from users.models import Student, RequestLog

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = "student"
    
class UserAdmin(BaseUserAdmin):
    inlines = [StudentInline]

class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'method', 'timestamp')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(RequestLog, RequestLogAdmin)
