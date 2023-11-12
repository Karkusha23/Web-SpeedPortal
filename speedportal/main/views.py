from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from main.models import Game, Category, AllowedCategory
from main.forms import RunForm

def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, "main/about.html")


def all_games(request):
    context = {
        'games': Game.objects.all(),
    }
    return render(request, 'main/allgames.html', context)

def game(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    context = {
        'game': game,
    }
    return render(request, 'main/game.html', context)


def run_upload(request):
    if request.method == 'POST':
        form = RunForm(data=request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, 'Вы успешно загрузили ран. Ожидайте одобрения модераторами')
            return HttpResponseRedirect(reverse('main:home'))
    else:
        if not request.user.is_authenticated:
            messages.error(request, 'Войдите в аккаунт, чтобы загружать раны')
            return HttpResponseRedirect(reverse('users:login'))
        form = RunForm()
    context = {
        'form': form
    }
    print(form.errors)
    return render(request, 'main/runupload.html', context)