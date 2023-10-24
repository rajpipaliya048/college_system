import datetime
from .forms import CourseForm
from .models import Course
from .models import Course, Enrollment
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.views.generic.list import ListView


class CreateCourseView(View):
    def get(self, request):
        if request.user.is_superuser:
            form = CourseForm()
            return render(request, 'course/create_course.html', {'form': form })
        else:
            return redirect('course:course_list')

    def post(self, request):
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            return HttpResponseRedirect('/course/list/')
        else:
            return render(request, 'course/create_course.html', {'form': form })

class CourseListView(ListView):
    model = Course
    
class CourseEnrollView(View):
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        student = self.request.user.student
        user = self.request.user
        course_id = self.request.POST.get('course_id')
        student = self.request.user.student           
        current_date = datetime.date.today()
        course_id = self.request.POST.get('course_id')
        course = get_object_or_404(Course, course_id=course_id)
        enrolled = Enrollment.objects.get_or_create(user_id=student, course_id=course, enrollment_date=current_date,)

        
        if course.fees != 0:    
            host = request.get_host()

            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": course.fees,
                "item_name": "name of the item",
                "currency_code": "USD",
                'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host,reverse('course:payment_done')),
                'cancel_return': 'http://{}{}'.format(host,reverse('course:payment_cancelled')),
            }
            form = PayPalPaymentsForm(initial=paypal_dict)
            return render(request, 'course/process_payment.html', {'course': course, 'form': form})
            
        else:
            obj = get_object_or_404(Enrollment, user_id=student, course_id=course_id)
            obj.isactive = True
            obj.save() 
        return redirect('dashboard')

@csrf_exempt
def payment_done(request):
    return render(request, 'course/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'course/payment_cancelled.html')

class CourseUnenrollView(View):
    def post(self, *args, **kwargs):
        course_id = self.request.POST.get('course_id')
        student = self.request.user.student
        obj = get_object_or_404(Enrollment, user_id=student, course_id=course_id)
        obj.isactive = False
        obj.save()
        return redirect('course:course_list')
   

def course_detail_view(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    return render(request, 'course/course_detail.html', {'course': course})
