from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from main.models import Game, Category, AllowedCategory, Run
from main.forms import RunForm
from users.models import User

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


@login_required
def run_upload(request):
    if request.method == 'POST':
        form = RunForm(data=request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, 'Вы успешно загрузили ран. Ожидайте одобрения модераторами')
            return HttpResponseRedirect(reverse('main:home'))
    else:
        form = RunForm()
    context = {
        'form': form
    }
    return render(request, 'main/runupload.html', context)

def run(request, run_id):
    context = {
        'run': Run.objects.get(id=run_id)
    }
    return render(request, 'main/run.html', context)