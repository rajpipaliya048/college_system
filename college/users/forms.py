import re
from django import forms
from django_countries.fields import CountryField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as __
from users.models import Student


def validate_number(value):
    if not re.match(r'^\d{10}$', value):
        raise ValidationError(
            __("Please enter valid mobile number"),
            params={"value": value},
        )
        
def validate_name(value):
    if not re.match(r'^[A-Za-z]+$', value):
        raise ValidationError(
            __("Please enter valid mobile number"),
            params={"value": value},
        )
        
def validate_age(value):
    if value <= 0:
        raise ValidationError(
            __("Please enter valid age"),
            params={"value": value},
        )
    
class StudentForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, min_length=3, validators=[validate_name])
    last_name = forms.CharField(max_length=50, min_length=3, validators=[validate_name])
    email = forms.EmailField()
    age = forms.IntegerField(validators=[validate_age])
    country = CountryField().formfield()
    mobile_number = forms.CharField(max_length=10, min_length=10, validators=[validate_number])
    gender_choice = (
        ("male", "male"),
        ("female", "female"),
    )
    gender = forms.ChoiceField(choices=gender_choice,)
    education_choice = (
        ('10th pass', '10th pass'),
        ('12th pass', '12th pass'),
        ('graduation', 'graduation'),
        ('post_graduation', 'post graduation'),        
    )
    level_of_education = forms.ChoiceField(choices=education_choice, required=True)
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2', 
                  'age', 'country', 'mobile_number', 'gender', 'level_of_education')
    
class UpdateProfileForm(ModelForm):
    
    age = forms.IntegerField(validators=[validate_age])
    country = CountryField().formfield()
    mobile_number = forms.CharField(max_length=10, min_length=10, validators=[validate_number])
    gender_choice = (
        ("male", "male"),
        ("female", "female"),
    )
    gender = forms.ChoiceField(choices=gender_choice,)
    education_choice = (
        ('10th pass', '10th pass'),
        ('12th pass', '12th pass'),
        ('graduation', 'graduation'),
        ('post_graduation', 'post graduation'),        
    )
    level_of_education = forms.ChoiceField(choices=education_choice, required=True)
    class Meta:
        model = Student
        fields = ('age', 'country', 'mobile_number', 'gender', 'level_of_education' )