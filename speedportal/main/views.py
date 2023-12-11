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
    if request.user.is_banned:
        return render(request, 'users/banscreen.html')
    context = {
        'form': form
    }
    return render(request, 'main/runupload.html', context)


def run(request, run_id):
    run = Run.objects.get(id=run_id)
    moderator = None
    if request.user.is_authenticated and not request.user.is_banned:
        moderator = Moderator.objects.filter(user=request.user, game=run.game_category.game) if not run.is_validated and not run.is_rejected else None
        moderator = moderator.first() if moderator and moderator.exists() else None
        if moderator and not moderator.can_validate_runs:
            moderator = None
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


def run_validation_post(request, run_id):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('main:run', kwargs={'run_id': run_id}))
    run = Run.objects.get(id=run_id)
    moderator = Moderator.objects.get(user=request.user, game=run.game_category.game)
    validation_form = ValidationForm(data=request.POST)
    if validation_form.is_valid():
        validation_form.save(run, moderator)
    else:
        messages.error(request, 'Ошибка: неверная форма валидации забега')
    return HttpResponseRedirect(reverse('main:run', kwargs={'run_id': run_id}))


def run_comment_post(request, run_id):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('main:run', kwargs={'run_id': run_id}))
    run = Run.objects.get(id=run_id)
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        comment_form.save(run, request.user)
    else:
        messages.error(request, 'Ошибка: неверная форма комментария')
    return HttpResponseRedirect(reverse('main:run', kwargs={'run_id': run_id}))


def run_report_post(request, run_id):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('main:run', kwargs={'run_id': run_id}))
    run = Run.objects.get(id=run_id)
    report_form = ReportForm(data=request.POST)
    if report_form.is_valid():
        report_form.save(run, request.user)
        messages.success(request, 'Вы успешно отправили жалобу. Модераторы в ближайшее время ее рассмотрят')
    else:
        messages.error(request, 'Ошибка: неверная форма жалобы')
    return HttpResponseRedirect(reverse('main:run', kwargs={'run_id': run_id}))


def user_runs(request, user_slug):
    context = {
        'user_to_show': User.objects.get(slug=user_slug)
    }
    return render(request, 'main/userruns.html', context)


@login_required
def unvalidated_runs(request):
    return render(request, 'main/unvalidatedruns.html')


@login_required
def moderation(request):
    moderators = request.user.get_moderators()
    if not moderators.exists():
        messages.error(request, 'Вы не являетесь модератором!')
        return HttpResponseRedirect(reverse('main:home'))
    if request.user.is_banned:
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