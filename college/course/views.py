import datetime
import paypalrestsdk
from .forms import CourseForm
from .models import Course
from .models import Course, Enrollment
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView

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

class CourseListView(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'course/course_list.html', {'courses': courses })
    

paypalrestsdk.configure({
    "mode": "sandbox", 
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})
class CourseEnrollView(View):
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        student = self.request.user.student
        course_id = self.request.POST.get('course_id')
        student = self.request.user.student           
        current_date = datetime.date.today()
        course_id = self.request.POST.get('course_id')
        course = get_object_or_404(Course, course_id=course_id)
        enrolled = Enrollment.objects.get_or_create(user_id=student, course_id=course, enrollment_date=current_date)
        if enrolled:
            obj = get_object_or_404(Enrollment, user_id=student, course_id=course_id)
            obj.isactive = True
            obj.save() 
        
        
        payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('course:execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('home')),
        },
        "transactions": [
            {
                "amount": {
                    "total": Course.objects.filter(course_id=course_id).values('fees'),
                    "currency": "INR",
                },
                "description": "Payment for Product/Service",
            }
        ],
        })
        if payment.create():
            return redirect(payment.links[1].href) 
        else:
            return render(request, 'payment_failed.html')

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'course/payment_success.html')
    else:
        return render(request, 'course/payment_failed.html')

def payment_checkout(request):
    return render(request, 'checkout.html')    
    
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
