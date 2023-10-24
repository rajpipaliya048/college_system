from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

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
            
            student = Student.objects.get_or_create(user=user, age=age, country=country, mobile_number=mobile_number, gender=gender, level_of_education=level_of_education)
                        
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

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
