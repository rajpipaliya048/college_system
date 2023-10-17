from django.shortcuts import render, redirect
from .forms import CourseForm


def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            return redirect('home')
    else:
        form = CourseForm()
    return render(request, 'course/create_course.html', { 'form': form })
