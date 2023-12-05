from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
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
                if user.is_banned:
                    return render(request, 'users/banscreen.html')
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


def profile(request, user_slug):
    user_to_show = User.objects.get(slug=user_slug)
    if request.user.is_authenticated and request.user.id != user_to_show.id and request.user.is_moderator():
        reports = user_to_show.get_relevant_reports_for(request.user)
    context = {
        'user_to_show': user_to_show,
        'reports': reports
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_change(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile', kwargs={'user_slug': request.user.slug}))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'users/profilechange.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:home'))


def user_runs(request, user_slug):
    context = {
        'user_to_show': User.objects.get(slug=user_slug)
    }
    return render(request, 'main/userruns.html', context)
