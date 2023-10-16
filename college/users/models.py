from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Student(models.Model):
    male ='male'
    female = 'female'
    
    ssc = '10th pass'
    hsc = '12th pass'
    graduation = 'graduation'
    post_graduation = 'post_graduation'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, primary_key=True)
    age = models.PositiveBigIntegerField()
    country = CountryField()
    mobile_number = models.IntegerField()
    gender_choice = [(male, "male"), (female, "female"),]
    gender = models.CharField(max_length=6, choices=gender_choice,)
    education_choice = [(ssc, '10th pass'), 
                        (hsc, '12th pass'), 
                        (graduation, "graduation"), 
                        (post_graduation, 'post_graduation'),
                        ]
    level_of_education = models.CharField(max_length=20, choices=education_choice,)
    
    def __str__(self):
        return self.user