from django.forms import ModelForm
from django import forms
from .models import Course
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = 'date'

class CourseForm(ModelForm):
    
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'course_details', 'department', 'course_img', 'start_course', 'end_course', 'fees', 'html_input']
        widgets = {
            'start_course': DateInput(),
            'end_course': DateInput(),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_course")
        end_date = cleaned_data.get("end_course")
        if end_date < start_date:
            raise ValidationError("End date should be greater than start date.")