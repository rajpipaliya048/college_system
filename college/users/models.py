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
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveBigIntegerField()
    country = CountryField()
    mobile_number = models.CharField(max_length=10)
    gender_choice = [(male, "male"), (female, "female"),]
    gender = models.CharField(max_length=6, choices=gender_choice,)
    education_choice = [(ssc, '10th pass'), 
                        (hsc, '12th pass'), 
                        (graduation, "graduation"), 
                        (post_graduation, 'post_graduation'),
                        ]
    level_of_education = models.CharField(max_length=20, choices=education_choice,)
    skills = models.TextField(null=True)
    
    def __str__(self):
        return self.user.username
    
class RequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username