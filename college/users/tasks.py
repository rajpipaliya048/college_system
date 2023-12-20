import csv
import os
from celery import shared_task
from course.models import Course, Enrollment
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from io import StringIO
from users.models import Student



@shared_task()
def update_user_details_from_csv(csv_data):
    csv_file = StringIO(csv_data)
    users = csv.DictReader(csv_file)
    for user in users:
        email = user['email']
        username = user['username']
        user = get_object_or_404(User, email=email)
        user.username = username
        user.save()
        student = Student.objects.filter(user=user).update(age = user['age'], 
                                                           country = user['country'], 
                                                           mobile_number = user['mobile_number'],
                                                           gender = user['gender'], 
                                                           level_of_education = user['level_of_education'], 
                                                           skills = user['skills'])

@shared_task()
def send_email_to_users(user, subject, message):
    email = EmailMessage(
    subject,
    message,
    "noreply@example.com",
    user,
    )
    email.send()
    
@shared_task()
def generate_csv_report():
    courses = Course.objects.all()
    enrollments = Enrollment.objects.select_related('user_id', 'course_id').filter(isactive=True)
    file_path = os.path.join(settings.BASE_DIR, 'report', 'enrollment_report.csv')
    
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['User ID', 'User Name', 'Course ID', 'Course Name', 'Course Details' , 'Enrollment Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for enrollment in enrollments:
            user_id = enrollment.user_id.user.id
            user_name = enrollment.user_id.user.username
            course_id = enrollment.course_id.course_id
            course_name = enrollment.course_id.course_name
            course_details = enrollment.course_id.course_details
            enrollment_date = enrollment.enrollment_date.strftime('%Y-%m-%d')
            
            writer.writerow({
                'User ID': user_id,
                'User Name': user_name,
                'Course ID': course_id,
                'Course Name': course_name,
                'Enrollment Date': enrollment_date,
                'Course Details': course_details
            })

    cache.set('report', True)