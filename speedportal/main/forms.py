from django import forms
from django.db.models import Subquery
from main.models import Game, Category, AllowedCategory, Run, Validation, Rejection, Comment, Report
from users.models import User

class RunForm(forms.Form):
    game = forms.ModelChoiceField(queryset=Game.objects.all().order_by('name'), required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    runtime_hours = forms.IntegerField(required=True, initial=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Часы'}))
    runtime_minutes = forms.IntegerField(required=True, initial=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Минуты'}))
    runtime_seconds = forms.IntegerField(required=True, initial=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Секунды'}))
    runtime_ms = forms.IntegerField(required=True, initial=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Миллисекунды'}))
    video_link = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Ссылка на видео'}))

    def game_category_is_valid(self):
        if not AllowedCategory.objects.filter(game=self.data['game'], category=self.data['category']).exists():
            self.errors['Игра/Категория: '] = 'Указанная категория недоступна для указанной игры'
            return False
        return True

    def runtime_is_valid(self):
        hours = int(self.data['runtime_hours'])
        minutes = int(self.data['runtime_minutes'])
        seconds = int(self.data['runtime_seconds'])
        ms = int(self.data['runtime_ms'])
        valid = True
        if hours < 0 or hours > 500:
            self.errors['Часы: '] = 'Некорректное значение'
            valid = False
        if minutes < 0 or minutes > 60:
            self.errors['Минуты: '] = 'Некорректное значение'
            valid = False
        if seconds < 0 or seconds > 60:
            self.errors['Секунды: '] = 'Некорректное значение'
            valid = False
        if ms < 0 or ms > 1000:
            self.errors['Миллисекунды: '] = 'Некорректное значение'
            valid = False
        return valid

    def is_valid(self):
        valid = super(RunForm, self).is_valid()
        game_category = self.game_category_is_valid()
        runtime = self.runtime_is_valid()
        return valid and game_category and runtime

    def get_runtime_ms(self):
        hours = int(self.data['runtime_hours'])
        minutes = int(self.data['runtime_minutes'])
        seconds = int(self.data['runtime_seconds'])
        ms = int(self.data['runtime_ms'])
        return hours * 3600000 + minutes * 60000 + seconds * 1000 + ms

    def save(self, user):
        Run.objects.create(game_category=AllowedCategory.objects.get(game=self.data['game'], category=self.data['category']),
                           user=user, runtime_ms=self.get_runtime_ms(), video_link=self.data['video_link'])


class ValidationForm(forms.Form):
    validate_choice = forms.ChoiceField(choices=((0, '------'),(1, 'Принять'), (2, 'Отклонить')), required=True)
    reject_reason = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Укажите причину отклонения забега'
    }))

    def save(self, run, moderator):
        if self.data['validate_choice'] == '1':
            run.is_validated = True
            points = run.get_points_for_run()
            user = User.objects.get(id=run.user_id)
            user.points += points
            user.save()
            Validation.objects.create(run=run, moderator=moderator, points=points)
        elif self.data['validate_choice'] == '2':
            run.is_rejected = True
            Rejection.objects.create(run=run, moderator=moderator, reason=self.data['reject_reason'])
        run.save()


class CommentForm(forms.Form):
    comment_text = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Напишите комментарий'
    }))

    def save(self, run, user):
        Comment.objects.create(run=run, user=user, comment_text=self.data['comment_text'])


class ReportForm(forms.Form):
    report_text = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Укажите причину жалобы'
    }))

    def save(self, run, user):
        Report.objects.create(run=run, user=user, report_text=self.data['report_text'])


class AllowedCategoryForm(forms.Form):
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.none())
    category_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Название категории'
    }))
    description = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Описание категории'
    }))

    def __init__(self, category_values=Category.objects.all().values('id'), *args, **kwargs):
        super(AllowedCategoryForm, self).__init__(*args, **kwargs)
        if category_values:
            self.fields['category'].queryset = Category.objects.filter(id__in=Subquery(category_values))

    def save(self, game):
        if self.data['category']:
            AllowedCategory.objects.create(game=game, category=Category.objects.get(id=self.data['category']), extra_description=self.data['description'])
        else:
            new_category = Category(name=self.data['category_name'])
            new_category.save()
            AllowedCategory.objects.create(game=game, category=new_category, extra_description=self.data['description'])