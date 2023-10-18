from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from .forms import CourseForm
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from users.models import Student

class CreateCourseView(View):
    # @user_passes_test(lambda u: u.is_superuser)
    def get(self, request):
        form = CourseForm()
        return render(request, 'course/create_course.html', {'form': form })

    def post(self, request):
        form = CourseForm(request.POST, request.FILES)
        # import pdb;pdb.set_trace()
        if form.is_valid():
            course = form.save()
            return HttpResponseRedirect('/course/list/')
        else:
            return render(request, 'course/create_course.html', {'form': form })

class CourseListView(View):
    def get(self, request):
        courses = Course.objects.all()
        student = get_object_or_404(Student, user=self.request.user.id)
        enrolled_or_not = Enrollment.objects.filter(user_id=student)
        return render(request, 'course/course_list.html', {'courses': courses })

class CourseEnrollView(View):
    
    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        student = get_object_or_404(Student, user=self.request.user.id)
        current_date = datetime.date.today()
        course_id = self.request.POST.get('course_id')
        course = get_object_or_404(Course, course_id=course_id)
        enrolled = Enrollment.objects.get_or_create(user_id=student, course_id=course, enrollment_date=current_date)
        return redirect('course_list')
    
    
class CourseUnenrollView(View):
    
    def post(self, *args, **kwargs):
        course_id = self.request.POST.get('course_id')
        student = get_object_or_404(Student, user=self.request.user.id)
        query = Enrollment.objects.filter(course_id=course_id)
        obj = get_object_or_404(query, user_id=student)
        obj.delete()
        return redirect('course_list') 