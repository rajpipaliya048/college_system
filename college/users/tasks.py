from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from users.models import Student
import csv


@shared_task()
def update_user_details_from_csv(csv_file):
    users = csv.DictReader(csv_file)
    for user in csv_file:
        print(user['username'])
        # username = user['username']
        # age = int(user['age'])
        # country = user['country']  
        # mobile_number = int(user['mobile_number'])
        # gender = user['gender']  
        # level_of_education = user['level_of_education']  
        # skills = user.get('skills', None)
        # user = User.objects.get_or_create(username=username)
        # student = Student.objects.update_or_create(
        #     user=user,
        #     defaults={
        #         'age': age,
        #         'country': country,
        #         'mobile_number': mobile_number,
        #         'gender': gender,
        #         'level_of_education': level_of_education,
        #         'skills': skills,
        #     }
        # ) 

@shared_task()
def send_email_to_users(user, subject, message):
    send_mail(subject, message, 'noreply@example.com', [user])