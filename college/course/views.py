from django.shortcuts import render, redirect
from .forms import CourseForm
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import datetime
from users.models import Student


@user_passes_test(lambda u: u.is_superuser)
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            courses = Course.objects.all()
            return render(request, 'course/course_list.html', { 'courses': courses })
    else:
        form = CourseForm()
    return render(request, 'course/create_course.html', { 'form': form })


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', { 'courses': courses })

@login_required(login_url="/login/")
def course_enroll(request):
    if request.method == 'POST':
        user = request.user
        student = Student.objects.get(user=user.id)
        current_date = datetime.date.today()
        course_id = request.POST.get('course_id')
        course = Course.objects.get(course_id=course_id)
        enrolled_course = Enrollment(user_id=student, course_id=course, enrollment_date=current_date)
        enrolled_course.save()
        courses = Course.objects.all()
        return render(request, 'course/course_list.html', { 'courses': courses })
