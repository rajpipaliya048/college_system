import csv
from .forms import StudentForm, UpdateProfileForm
from .models import Student
from course.models import Enrollment
from .tokens import account_activation_token
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from users.tasks import update_user_details_from_csv, send_email_to_users



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
            skills = form.cleaned_data['skills']
            student = Student.objects.get_or_create(user=user, 
                                                    age=age, 
                                                    country=country, 
                                                    mobile_number=mobile_number, 
                                                    gender=gender, 
                                                    level_of_education=level_of_education, 
                                                    skills=skills
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
            return redirect('home')
        return render(request, 'users/login.html', {'form': form})
    
def update_skills(request):
    if request.method == 'POST':
        student = request.user.student
        student.skills = request.POST.get('skills')
        student.save()
        return redirect('dashboard')
    return render(request, 'users/update_skills.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

@login_required
def user_profile(request):
    student = request.user.student
    return render(request, 'users/user_profile.html', {'student': student})

# class EditProfileView(View):
    
#     @method_decorator(login_required)
#     def get(self, request):
#         user = request.user
#         student = self.request.user.student
#         form = UpdateProfileForm(initial={'age': student.age, 
#                                     'email': student.user.email, 
#                                     'first_name': student.user.first_name, 
#                                     'last_name': student.user.last_name, 
#                                     'country': student.country, 
#                                     'mobile_number': student.mobile_number, 
#                                     'gender': student.gender, 
#                                     'level_of_education': student.level_of_education
#                                     })
#         return render(request, 'users/profile_update.html', {'form': form})
    
#     @method_decorator(login_required)
#     def post(self, request):
#         form = UpdateProfileForm(request.POST)
#         if form.is_valid():
#             user = request.user
#             student = self.request.user.student
            
#             student.user.first_name = form.cleaned_data['first_name']
#             student.user.last_name = form.cleaned_data['last_name']
#             student.age = form.cleaned_data['age']
#             student.country = form.cleaned_data['country']
#             student.mobile_number = form.cleaned_data['mobile_number']
#             student.gender = form.cleaned_data['gender']
#             student.level_of_education = form.cleaned_data['level_of_education']
#             student.save()
#             global new_email
#             new_email = form.cleaned_data['email']
            
#             if student.user.email != new_email:
#                 current_site = get_current_site(request)
#                 subject = 'Activate your account'
#                 message = render_to_string('users/email_updation_email.html', {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': account_activation_token.make_token(user),
#                 })
#                 user.email_user(subject, message)
#                 return redirect('email_update_sent')
#             return redirect('dashboard')
        

class EditProfileView(UpdateView):

    model = Student
    form_class = UpdateProfileForm
    template_name = 'users/profile_update.html'
    
    def get_object(self):
        return self.request.user.student
    
    success_url ="/profile"
    
@login_required
def email_update_sent(request):
    return render(request, 'users/email_update_sent.html')

def update(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Student.DoesNotExist, Exception):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # user.email = new_email
        user.save()
        login(request, user)
        return redirect('email_updated')
    else:
        return HttpResponseBadRequest('link is invalid!')

@login_required
def email_updated(request):
    return render(request, 'users/email_updated.html')

@csrf_exempt
def update_users_from_csv(request):
    if request.method == 'GET':
        return render(request, 'users/update_user_from_csv.html')
    
    if request.method == 'POST':
        csv_file = request.FILES["csv_input"]
        if not csv_file.name.endswith('.csv'):
            return HttpResponseRedirect(reverse("update_users_from_csv"))
        file_data = csv_file.read().decode("utf-8")
        print(file_data)
        update_user_details_from_csv.delay(file_data)
        return redirect('/')

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        message = request.POST['message']
        subject = request.POST['subject']
        enrollments = Enrollment.objects.all()
        enrolled_users_emails = [enrollment.user_id.user.email for enrollment in enrollments]
        for user in enrolled_users_emails:
            send_email_to_users(user, subject, message)
        return redirect('/')
    return render(request, 'users/send_mass_mail.html')