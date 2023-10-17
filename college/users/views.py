from django.shortcuts import render, redirect
from .forms import StudentForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from course.models import Course, Enrollment
from users.models import Student

def signup_view(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user[0])
            return render(request, 'index.html')

    else:
        form = StudentForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            loggedin_user = request.user
            student = Student.objects.get(user=loggedin_user.id)
            enrolled_course = Enrollment.objects.all().filter(user_id = student).values('course_id_id')
            courses = []
            for i in enrolled_course:
                course_id = i['course_id_id']
                course = Course.objects.get(course_id=course_id)
                courses.append(course)
            return render(request, 'dashboard.html', { 'courses': courses })
        
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')