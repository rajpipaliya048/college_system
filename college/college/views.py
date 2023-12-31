from course.models import Course, Enrollment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from users.models import Student

@login_required
def dashboard(request):
    user = request.user
    if not user.is_superuser:
        student = get_object_or_404(Student, user=user.id)
        enrolled_course = Enrollment.objects.filter(user_id = student, isactive=True).values('course_id_id')
        courses = []
        for i in enrolled_course:
            course_id = i['course_id_id']
            course = get_object_or_404(Course, course_id=course_id)
            courses.append(course)
        return render(request, 'dashboard.html', { 'courses': courses })
    else:
        courses = []
        return render(request, 'dashboard.html', { 'courses': courses })
