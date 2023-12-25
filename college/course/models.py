import re
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse
from users.models import Student


def validate_course_id(value):
    reg = re.compile('^\d{2}[A-Z]{2}\d{2}$')
    if not reg.match(value) :
        raise ValidationError('%s should be start with 2 digits following by 2 capital letters and ends with 2 digits' % value)


class Department(models.Model):
    department_name = models.CharField(max_length=50, unique=True)
    departmrnt_slug = models.SlugField(max_length=10)
    
    def __str__(self):
        return self.department_name

class CourseManager(models.Manager):
    def free_courses(self):
        return super().get_queryset().filter(fees=0)

class Course(models.Model):
    course_id = models.CharField(max_length=6, primary_key=True, validators=[validate_course_id])
    course_name = models.CharField(max_length=256)
    course_details = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_img = models.ImageField(blank=True, upload_to='course-images/')
    start_course = models.DateField(null=True)
    end_course = models.DateField(null=True)    
    fees = models.PositiveIntegerField(default=0)
    html_input = models.TextField(null=True)
    
    objects = CourseManager()
    
    def __str__(self):
        return self.course_id
    
    def snippet_title(self):
        return self.course_name[:30] + '...'
    
    def snippet(self):
        return self.course_details[:70] + '...'  
    
class EnrollsManager(models.Manager):
    def active_enrolls(self):
        return super().get_queryset().filter(isactive=True)

class Enrollment(models.Model):
    user_id = models.ForeignKey(Student, on_delete= models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete= models.CASCADE)
    enrollment_date = models.DateField()
    isactive = models.BooleanField(default=True)
    
    objects = EnrollsManager()
    
    
    def __str__(self):
        return self.user_id.user.username
    
