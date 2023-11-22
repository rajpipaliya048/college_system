from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from users.models import Student
import csv
from django.shortcuts import get_object_or_404
from io import StringIO


@shared_task()
def update_user_details_from_csv(csv_data):
    csv_file = StringIO(csv_data)
    users = csv.DictReader(csv_file)
    for user in users:
        email = user['email']
        username = user['username']
        age = user['age']
        country = user['country']  
        mobile_number = user['mobile_number']
        gender = user['gender']  
        level_of_education = user['level_of_education']  
        skills = user.get('skills', None)
        user = get_object_or_404(User, email=email)
        user.username = username
        user.save()
        student = get_object_or_404(Student, user=user)
        student.age = age
        student.country = country
        student.mobile_number = mobile_number
        student.gender = gender
        student.level_of_education = level_of_education
        student.skills = skills
        student.save()

@shared_task()
def send_email_to_users(user, subject, message):
    send_mail(subject, message, 'noreply@example.com', [user])