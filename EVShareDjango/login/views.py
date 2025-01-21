import random
import string

from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,reverse

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.http.response import JsonResponse
from django.core.mail import send_mail

from . import forms
from system.models import User
from .forms import UserProfileForm
from .models import CaptchaModel


@require_http_methods(['GET','POST'])
def EVSlogin(request):
    if request.method == 'GET':
        form = forms.LoginForm()
        return render(request, 'log_in.html', context={'form':form})
    else:
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            usertype = request.POST.get('userType')
            try:
                user = User.objects.get(username=username, password=password, userType=usertype)
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect(reverse('index'))
            except User.DoesNotExist:
                form.add_error('username', 'Wrong account or password')
                return render(request, 'log_in.html', context={'form': form})
        else:
            return render(request, 'log_in.html')

@require_http_methods(['GET'])
def EVSlogout(request):
    logout(request)
    return redirect(reverse('index'))

@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            surname = form.cleaned_data['surname']
            firstname = form.cleaned_data['firstname']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            user = User(
                username=username,
                password=password,
                surname=surname,
                firstname=firstname,
                email=email,
                telephone=telephone)
            user.save()
            print(f'username: {username}, password: {password},  surname: {surname}'
                  f', firstname: {firstname}, email: {email}, phone: {telephone}')
            return redirect(reverse('index'))
        else:
            print(form.errors)
            return render(request, 'register.html', {'form': form})

def send_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code":400,"message":"email is required"})
    captcha = "".join(random.sample(string.digits,4))
    CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})
    send_mail(subject="Your verification code",message=f"Your verification code is {captcha}",from_email=None,
              recipient_list=[email])
    return JsonResponse({'code':200,'message':f'code sent to {email}'})


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')  # Assuming 'profile' is the name of the profile URL
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form, 'user': user})


