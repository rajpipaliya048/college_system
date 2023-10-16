from django.contrib import admin
from .models import Course
from .models import Department
from .models import Enrollment


admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Enrollment)
