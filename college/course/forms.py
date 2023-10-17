from django.forms import ModelForm
from django import forms
from .models import Course


class DateInput(forms.DateInput):
    input_type = 'date'


class CourseForm(ModelForm):
    
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'course_details', 'department', 'course_img', 'start_course', 'end_course']
        widgets = {
            'start_course': DateInput(),
            'end_course': DateInput(),
        }