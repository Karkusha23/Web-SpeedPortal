from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:home'))
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'users/registration.html', context)

def profile(request):
    context = {

    }
    return render(request, 'users/profile.html', context)

def profile_change(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'users/profilechange.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:home'))