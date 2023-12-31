import logging
import os
from course.models import Course
from course.models import Enrollment
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.http import HttpResponseBadRequest, HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic.edit import UpdateView
from users.decorators import superuser_required
from users.forms import StudentForm, UpdateProfileForm
from users.models import Student
from users.tasks import update_user_details_from_csv, send_email_to_users, generate_csv_report
from users.tokens import account_activation_token

logger = logging.getLogger(__name__)
# signup view
class SignupView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = StudentForm()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            age = form.cleaned_data['age']
            country = form.cleaned_data['country']
            mobile_number = form.cleaned_data['mobile_number']
            gender = form.cleaned_data['gender']
            level_of_education = form.cleaned_data['level_of_education']
            # skills = form.cleaned_data['skills']
            student = Student.objects.get_or_create(user=user, 
                                                    age=age, 
                                                    country=country, 
                                                    mobile_number=mobile_number, 
                                                    gender=gender, 
                                                    level_of_education=level_of_education, 
                                                    )
                        
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            
            return redirect('account_activation_sent')
        return render(request, 'users/signup.html', {'form': form})

# login view
class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'users/login.html', {'form': form})
    
def update_skills(request):
    if request.method == 'POST':
        student = request.user.student
        student.skills = request.POST.get('skills')
        student.save()
        return redirect('dashboard')
    return render(request, 'users/update_skills.html')


# logout view
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
     
# edit student data by user(student)
class EditProfileView(UpdateView):

    model = Student
    form_class = UpdateProfileForm
    template_name = 'users/profile_update.html'
    
    def get_object(self):
        return self.request.user.student
    
    success_url ="/profile"
    

# admin actions views
@method_decorator(superuser_required, name='dispatch')
class UpdateUserFromCsv(View):
    def get(self, request):
        return render(request, 'users/update_user_from_csv.html')

    
    def post(self, request):
        csv_file = request.FILES["csv_input"]
        if not csv_file.name.endswith('.csv'):
            return HttpResponseRedirect(reverse("update_users_from_csv"))
        file_data = csv_file.read().decode("utf-8")
        update_user_details_from_csv.delay(file_data)
        logger.info("user data updated with the use of csv")
        return redirect('/')
    
   
@method_decorator(superuser_required, name='dispatch')
class SendEmail(View):
    
    def get(self, request):
        courses = Course.objects.all()
        course_ids = [course.course_id for course in courses]
        return render(request, 'users/send_mass_mail.html', {'course_ids': course_ids})
    
    def post(self, request):
        message = request.POST.get('message', 'Default message')
        subject = request.POST.get('subject', 'Default subject')
        course_list = request.POST.get('course_list')
        course = course_list.split(',')
        logger.info("Sending Email started") 
        enrolled_users_emails = []
        for course_id in course:
            enrollments = Enrollment.objects.filter(course_id=course_id)
            for enrollment in enrollments:
                enrolled_users_emails.append(enrollment.user_id.user.email)
        send_email_to_users.delay(enrolled_users_emails, subject, message)
        return redirect('/')
    
@method_decorator(superuser_required, name='dispatch')
class CsvReport(View):
    def get(self, request):
        data = cache.get('report')
        if not data:
            generate_csv_report.delay()
            logger.info("New csv report generated") 

        file = os.path.join(settings.BASE_DIR, 'report/enrollment_report.csv')
        fileopened = open(file, 'rb')
        return FileResponse(fileopened)
    
@method_decorator(superuser_required, name='dispatch')
class Actions(View):
    def get(self, request):
        return render(request, 'actions.html')
    
    
@method_decorator(superuser_required, name='dispatch')
class PaymentSelectionView(View):
    def get(self, request):
        return render(request, 'users/payment_selection.html')
    
    def post(self, request):
        payment_gateway = self.request.POST.get('gateway')
        request.session['payment_gateway'] = payment_gateway
        return redirect('home')
    
    
# end of admin actions views

@login_required
def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Student.DoesNotExist, Exception):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account_activation_complete')
    else:
        return HttpResponseBadRequest('Activation link is invalid!')

@login_required
def account_activation_complete(request):
    return render(request, 'users/account_activation_complete.html')

@login_required
def user_profile(request):
    if not request.user.is_superuser:
        student = request.user.student
        return render(request, 'users/user_profile.html', {'student': student})
    return render(request, 'users/user_profile.html',)

@login_required
def email_update_sent(request):
    return render(request, 'users/email_update_sent.html')

def update_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Student.DoesNotExist, Exception):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.save()
        login(request, user)
        return redirect('email_updated')
    else:
        return HttpResponseBadRequest('link is invalid!')

@login_required
def email_updated(request):
    return render(request, 'users/email_updated.html')
