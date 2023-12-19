from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Subquery
from django.core import serializers
from users.models import User, Moderator
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, BanForm, ModeratorForm
from main.models import Game


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
    moderators_json = serializers.serialize('json', request.user.get_moderators()) if request.user.is_authenticated else None
    ban_form = BanForm()
    moderator_form = ModeratorForm(request.user.get_relevant_moderators_ids(user_to_show)) if request.user.is_authenticated else None
    if moderator_form and moderator_form.fields['game'].queryset.count() == 0:
        moderator_form = None
    reports = None
    if request.user.is_authenticated and request.user.id != user_to_show.id and request.user.is_moderator():
        reports = user_to_show.get_relevant_reports_for(request.user)
    context = {
        'user_to_show': user_to_show,
        'reports': reports,
        'ban_form': ban_form,
        'moderators_json': moderators_json,
        'moderator_form': moderator_form
    }
    return render(request, 'users/profile.html', context)


def profile_ban_post(request, user_slug):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('users:profile', kwargs={'user_slug': user_slug}))
    user_to_show = User.objects.get(slug=user_slug)
    ban_form = BanForm(data=request.POST)
    if ban_form.is_valid():
        ban_form.save(user_to_show, Moderator.objects.filter(user=request.user).first())
        messages.success(request, 'Пользователь успешно забанен')
    else:
        messages.error(request, 'Ошибка: неверная форма бана')
    return HttpResponseRedirect(reverse('users:profile', kwargs={'user_slug': user_slug}))


def profile_moderator_post(request, user_slug):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('users:profile', kwargs={'user_slug': user_slug}))
    user_to_show = User.objects.get(slug=user_slug)
    moderator_form = ModeratorForm(data=request.POST)
    if moderator_form.is_valid():
        moderator_form.save(user_to_show)
        messages.success(request, f'Вы успешно повысили {user_to_show.username} до модератора')
    else:
        messages.error(request, 'Ошибка: неверная форма повышения до модератора')
    return HttpResponseRedirect(reverse('users:profile', kwargs={'user_slug': user_slug}))



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
