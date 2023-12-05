from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from main.models import Game, Category, AllowedCategory, Run
from main.forms import RunForm, ValidationForm, CommentForm, ReportForm
from users.models import User, Moderator

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
    if user.is_banned:
        return render(request, 'users/banscreen.html')
    context = {
        'form': form
    }
    return render(request, 'main/runupload.html', context)


def run(request, run_id):
    run = Run.objects.get(id=run_id)
    moderator = Moderator.objects.filter(user=request.user, game=run.game_category.game) if request.user.is_authenticated and not run.is_validated and not run.is_rejected else None
    moderator = moderator.first() if moderator else None
    if request.method == 'POST':
        validation_form = ValidationForm(data=request.POST)
        comment_form = CommentForm(data=request.POST)
        report_form = ReportForm(data=request.POST)
        if validation_form.is_valid():
            validation_form.save(run, moderator)
            return HttpResponseRedirect(reverse('main:run', kwargs={'run_id': run.id}))
        elif comment_form.is_valid():
            comment_form.save(run, request.user)
            return HttpResponseRedirect(reverse('main:run', kwargs={'run_id': run.id}))
        elif report_form.is_valid():
            report_form.save(run, request.user)
            messages.success(request, 'Вы успешно отправили жалобу. Модераторы в ближайшее время ее рассмотрят')
            return HttpResponseRedirect(reverse('main:run', kwargs={'run_id': run.id}))
    else:
        validation_form = ValidationForm()
        comment_form = CommentForm()
        report_form = ReportForm()
    context = {
        'run': run,
        'moderator': moderator,
        'validation_form': validation_form,
        'comment_form': comment_form,
        'report_form': report_form
    }
    return render(request, 'main/run.html', context)


@login_required
def moderation(request):
    moderators = request.user.get_moderators()
    if not moderators.exists():
        messages.error(request, 'Вы не являетесь модератором!')
        return HttpResponseRedirect(reverse('main:home'))
    if user.is_banned:
        return render(request, 'users/banscreen.html')
    context = {
        'moderators': moderators
    }
    return render(request, 'main/moderation.html', context)


def leaderboard(request, game_slug, category_slug):
    game = Game.objects.get(slug=game_slug)
    category = Category.objects.get(slug=category_slug)
    game_category = AllowedCategory.objects.filter(game=game, category=category)
    if not game_category.exists():
        messages.error(request, 'Эта категория недоступна для этой игры!')
        return HttpResponseRedirect(reverse('main:home'))
    game_category = game_category.first()
    context = {
        'game_category': game_category
    }
    return render(request, 'main/leaderboard.html', context)