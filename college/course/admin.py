from django.contrib import admin
from .models import Course
from .models import Department
from .models import Enrollment

class EnrollmentAdmin(admin.ModelAdmin):
  list_display = ("user_id", "course_id", "enrollment_date", "isactive")



admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Enrollment, EnrollmentAdmin)
