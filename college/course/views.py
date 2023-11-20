import datetime
import random
import razorpay
import requests
import stripe
import time
from course.forms import CourseForm
from course.models import Course, Enrollment
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from paypal.standard.forms import PayPalPaymentsForm

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CreateCourseView(View):
    def get(self, request):
        form = CourseForm()
        return render(request, 'course/create_course.html', {'form': form })

    def post(self, request):
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            return HttpResponseRedirect('/course/list/')
        else:
            return render(request, 'course/create_course.html', {'form': form })

class CourseListView(ListView):
    model = Course
    paginate_by = 3
class CourseEnrollView(View):
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        student = self.request.user.student
        course_id = self.request.POST.get('course_id')
        student = self.request.user.student           
        current_date = datetime.date.today()
        course = get_object_or_404(Course, course_id=course_id)
        enrolled = Enrollment.objects.get_or_create(user_id=student, course_id=course, enrollment_date=current_date,)
        fees = course.fees * 100
        order_id = generate_unique_order_id()
        if course.fees != 0:    
            return render(request, 'course/payment_form.html', {'course_id': course.course_id, 'amount': fees, 'order_id': order_id}) 
            
        else:
            obj = get_object_or_404(Enrollment, user_id=student, course_id=course_id)
            obj.isactive = True
            obj.save() 

@csrf_exempt
def payment_done(request):
    return render(request, 'course/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'course/payment_cancelled.html')

class PaypalPaymentView(View):
    def post(self, request):
        course_id = self.request.POST.get('course_id')
        course = get_object_or_404(Course, course_id=course_id)
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
    
class StripePaymentView(View):
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        course_id = self.request.POST.get('course_id')
        course = get_object_or_404(Course, course_id=course_id)
        amount = int(course.fees)
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',  
                    'unit_amount': amount,
                    'product_data': {
                        'name': 'Course Payment',
                        'description': 'Enroll in the course',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url= "http://www.mycollege.com:8000/dashboard", 
        )
        return redirect('dashboard')
 

def initiate_razorpay_payment(request):
    if request.method == "POST":
        amount = int(request.POST["amount"]) * 100

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        payment_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "order_receipt",
            "notes": {
                "email": "user_email@example.com",
            },
        }

        order = client.order.create(data=payment_data)
        
        response_data = {
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key": settings.RAZORPAY_API_KEY,
            "name": "college",
            "description": "Payment for Your Product",
        }
        
        return redirect('dashboard')
    
    return render(request, "payment.html")

def initiate_cashfree_payment(request):
    course_id = request.POST.get('course_id')
    course = get_object_or_404(Course, course_id=course_id)
    total_amount = course.fees
    order_id = request.POST.get('order_id')
    merchant_id = settings.CASHFREE_CLIENT_ID
    secret_key = settings.CASHFREE_CLIENT_SECRET
    payment_url = 'https://sandbox.cashfree.com/pg/orders'

    payload = {
        "customer_details": {
            "customer_id": request.user.username,
            'customer_name': request.user.first_name,
            'customer_email': request.user.email,
            'customer_phone': str(request.user.student.mobile_number),
        },
        "order_meta": {
            "return_url": 'http://www.mycollege.com:8000/course/success/',
            "notify_url": 'http://www.mycollege.com:8000/course/notify/', 
        },
        'order_id': order_id,  
        'order_amount': str(total_amount),
        'order_currency': 'INR',
        'order_note': 'Payment for Course Enrollment',
    }
    headers = {
    "accept": "application/json",
    "x-api-version": "2022-09-01",
    "content-type": "application/json",
    "x-client-id": merchant_id,
    "x-client-secret": secret_key
}
    response = requests.post(payment_url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        payment_session_id = data['payment_session_id']
        order_id = data['order_id']
        return render(request, 'course/cashfree_payment.html', {'payment_session_id': payment_session_id, 'order_id': order_id })
    else:
        return JsonResponse({'error': 'Failed to initiate payment'})

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


def generate_unique_order_id():
    timestamp = int(time.time() * 1000)
    random_number = random.randint(1000, 9999)
    order_id = f"{timestamp}{random_number}"
    return order_id