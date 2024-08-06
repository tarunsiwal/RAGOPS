from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('base')
        elif user is not None and not user.is_active:
            messages.error(request, 'Your account is inactive. Please contact support.')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def token(request):
    return render(request , 'token.html')

def success (request):
    return render(request , 'success.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect(reverse('signup'))
        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username is taken.')
                return redirect(reverse('signup'))
            elif User.objects.filter(email=email).first():
                messages.error(request, 'Email is taken.')
                return redirect(reverse('signup'))

            user = User.objects.create_user(username=username, email=email, password=password)

            profile_obj = Profile.objects.create(user=user, auth_token=str(uuid.uuid4()), is_verified=False)
            profile_obj.save()
            send_mail_after_registration(email, str(profile_obj.auth_token))

            messages.success(request, 'Registration successful. Please check your email for verification.')
            return redirect(reverse('token') + f'?my_variable={email}')

        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred during registration.')
            return redirect(reverse('signup'))

    return render(request, 'signup.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'You account is been verified')
            return redirect(reverse('login'))
        else:
            return redirect(reverse('error'))
    except Exception as e:
        print(e)


def error(request):
    return render(request, 'error.html')   


def send_mail_after_registration(email, auth_token):
    try:
        subject = "Your account needs to be verified"
        message = f'Hi, please click the following link to verify your account: http://127.0.0.1:8000/verify/{auth_token}'
        from_email = 'your_email@example.com'  # Replace with your email address or use a valid one
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
