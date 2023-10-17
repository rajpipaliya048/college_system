from django.shortcuts import render
from course.models import Course, Enrollment
from users.models import Student
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index.html')

@login_required(login_url="/login/")
def dashboard(request):
    user = request.user
    student = Student.objects.get(user=user.id)
    enrolled_course = Enrollment.objects.all().filter(user_id = student).values('course_id_id')
    courses = []
    for i in enrolled_course:
        course_id = i['course_id_id']
        course = Course.objects.get(course_id=course_id)
        courses.append(course)
    return render(request, 'dashboard.html', { 'courses': courses })
