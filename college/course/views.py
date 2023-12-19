import datetime
import razorpay
import requests
import stripe
from course.forms import CourseForm
from course.models import Course, Enrollment
from course.serializers import CourseSerializer
from course.utility import generate_unique_order_id
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from paypal.standard.forms import PayPalPaymentsForm
from rest_framework.generics import RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, BasePermission

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
    paginate_by = 15
class CourseEnrollView(View):
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        payment_gateway = request.session.get('payment_gateway') 
        print('\n'*5)
        print(payment_gateway)
        print('\n'*5)           
        student = self.request.user.student
        course_id = self.request.POST.get('course_id')
        student = self.request.user.student           
        current_date = datetime.date.today()
        course = get_object_or_404(Course, course_id=course_id)
        enrolled = Enrollment.objects.get_or_create(user_id=student, course_id=course, enrollment_date=current_date)
        fees = course.fees * 100
        order_id = generate_unique_order_id()
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
        if course.fees != 0:    
            if payment_gateway == 'paypal':
                return render(request, 'course/paypal_payment_form.html', {'course_id': course.course_id, 'amount': fees, 'order_id': order_id, 'form': form})
            if payment_gateway == 'stripe':
                return render(request, 'course/stripe_payment_form.html', {'course_id': course.course_id, 'amount': fees, 'order_id': order_id})
            if payment_gateway == 'cashfree':
                return render(request, 'course/cashfree_payment_form.html', {'course_id': course.course_id, 'amount': fees, 'order_id': order_id})
            if payment_gateway == 'razorpay':
                return render(request, 'course/razorpay_payment_form.html', {'course_id': course.course_id, 'amount': fees, 'order_id': order_id})
            return render(request, 'course/payment_form.html', {'course_id': course.course_id, 'amount': fees, 'order_id': order_id, 'form': form}) 
            return render(request, 'course/payment_form.html', {'course_id': course.course_id, 'amount': fees, 'order_id': order_id, 'form': form})
        else:
            obj = get_object_or_404(Enrollment, user_id=student, course_id=course_id)
            obj.isactive = True
            obj.save() 
            return redirect('dashboard')

    
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
 
class CourseUnenrollView(View):
    def post(self, *args, **kwargs):
        course_id = self.request.POST.get('course_id')
        student = self.request.user.student
        obj = get_object_or_404(Enrollment, user_id=student, course_id=course_id)
        obj.isactive = False
        obj.save()
        return redirect('home')

class SuperuserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class CourseAPIView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,GenericAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'course_id'
    permission_classes = [IsAuthenticated, SuperuserPermission]
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CourseListAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'course_id'
    permission_classes = [IsAuthenticated, SuperuserPermission]
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, SuperuserPermission]

   
# function based views
def course_detail_view(request, course_id):
    course = Course.objects.get(course_id=course_id)
    enrolled_status = Enrollment.objects.filter(course_id=course_id, user_id = request.user.student, isactive=True)
    context = {
        'course': course,
        'enrolled_status': enrolled_status,
    }
    return render(request, 'course/course_detail.html', context)

@csrf_exempt
def payment_done(request):
    return redirect('dashboard')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'course/payment_cancelled.html')

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